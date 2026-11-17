# VCAI App Standard: Encrypting Personal Data (PII)

**Applies to:** every app hosted on the VCAI Mac Studio (valleychristianai.com).
**Short version:** PII must be encrypted at rest using **AES-256-GCM field-level encryption**, with keys in environment variables and **HMAC-SHA256 blind indexes** for lookups.

Students run many kinds of code on the Studio. Encryption keeps a list of Valley
emails from being downloaded somewhere by accident. A new app must follow this
standard before it goes live. Otherwise, ask Mr. Mull (bmull@vcs.net) to encrypt
its data after launch.

## Apps already encrypted

Peer Tutor, BusTrackr, and 273Kelvin already encrypt their data. Each app has
its own keys, stored on the Studio and used there for decryption. Do not copy,
print, or reuse them.

On the Studio, [`secret/pii-keys.md`](secret/README.md) in this repository's
checkout lists where each app keeps its keys. If that file is missing, find the
app's environment file and key names yourself. List only the variable names,
never the values. These apps named their keys before the `PII_KEY` name used
below existed. Keep the names they already use.

## Rules

1. **What counts as PII:** names (students, parents, staff), emails, phone numbers, addresses, and any free-text field that holds them.
2. **Encrypt each field** with AES-256-GCM, using a fresh random 12-byte nonce for every value. Store it as text: `e1:` + base64(nonce + ciphertext + tag).
3. **Need to look it up?** (e.g. sign-in by email) Also store `email_h` = HMAC-SHA256 of the normalized value (trimmed, lowercased), derived from the same key, and search on `email_h`, never on plaintext.
4. **One key per app.** Generate a 32-byte random key per app. Never share keys between apps.
5. **Key lives only in the server environment** (`.env`, e.g. `PII_KEY`), never in code, git, the database, logs, or the browser. Add `.env` to `.gitignore`.
6. **Fail closed:** the app must refuse to start if the key is missing or the wrong length.
7. **Decrypt only on the server**, only when displaying to an authorized user. Never log decrypted values.
8. **Every write path encrypts**, including sign-ups, edits, imports and admin tools. Before launch, create a test account and confirm the database shows `e1:` values.
9. **Back up the key** with the VCAI admin (Mr. Mull). Losing the key means losing the data.
10. **Known limits:** you can't sort or search by partial name in SQL; do that in the app after decrypting. Files (PDFs, uploads) need separate protection.

Generate a key:
```bash
python3 -c "import secrets,base64;print(base64.b64encode(secrets.token_bytes(32)).decode())"
```

## Python (pip install cryptography)

```python
import os, base64, hmac, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_raw = base64.b64decode(os.environ.get("PII_KEY", ""))
if len(_raw) != 32:
    raise SystemExit("PII_KEY missing or not 32 bytes; refusing to start")
ENC_KEY = hmac.new(_raw, b"enc", hashlib.sha256).digest()
IDX_KEY = hmac.new(_raw, b"idx", hashlib.sha256).digest()
_aes = AESGCM(ENC_KEY)

def seal(text: str) -> str:
    if text is None or text.startswith("e1:"):
        return text
    nonce = os.urandom(12)
    return "e1:" + base64.b64encode(nonce + _aes.encrypt(nonce, text.encode(), None)).decode()

def open_(value: str) -> str:
    if not value or not value.startswith("e1:"):
        return value
    blob = base64.b64decode(value[3:])
    return _aes.decrypt(blob[:12], blob[12:], None).decode()

def blind_index(value: str) -> str:
    return hmac.new(IDX_KEY, value.strip().lower().encode(), hashlib.sha256).hexdigest()

# Save:   INSERT INTO users (name, email, email_h) VALUES (?, ?, ?)
#         (seal(name), seal(email), blind_index(email))
# Lookup: SELECT * FROM users WHERE email_h = ?   (blind_index(typed_email))
```

## Node.js (built-in crypto, no packages)

```js
const crypto = require("crypto");

const raw = Buffer.from(process.env.PII_KEY || "", "base64");
if (raw.length !== 32) { console.error("PII_KEY missing or not 32 bytes; refusing to start"); process.exit(1); }
const ENC_KEY = crypto.createHmac("sha256", raw).update("enc").digest();
const IDX_KEY = crypto.createHmac("sha256", raw).update("idx").digest();

function seal(text) {
  if (text == null || text.startsWith("e1:")) return text;
  const nonce = crypto.randomBytes(12);
  const c = crypto.createCipheriv("aes-256-gcm", ENC_KEY, nonce);
  const ct = Buffer.concat([c.update(text, "utf8"), c.final()]);
  return "e1:" + Buffer.concat([nonce, ct, c.getAuthTag()]).toString("base64");
}

function open(value) {
  if (!value || !value.startsWith("e1:")) return value;
  const b = Buffer.from(value.slice(3), "base64");
  const d = crypto.createDecipheriv("aes-256-gcm", ENC_KEY, b.subarray(0, 12));
  d.setAuthTag(b.subarray(b.length - 16));
  return Buffer.concat([d.update(b.subarray(12, b.length - 16)), d.final()]).toString("utf8");
}

function blindIndex(value) {
  return crypto.createHmac("sha256", IDX_KEY).update(value.trim().toLowerCase()).digest("hex");
}

module.exports = { seal, open, blindIndex };
```

Both versions produce the same `e1:` format, so a Python app and a Node app can read each other's data if they're given the same key.

## Launch checklist

- [ ] Key generated, in `.env` only, `.env` git-ignored, copy given to the VCAI admin
- [ ] App refuses to start without the key
- [ ] Every PII write uses `seal()`; lookups use `email_h`
- [ ] Test account shows `e1:` values in the database
- [ ] No PII in logs, error messages, or client-side code
