# Contributing to Studio-hosted incubator apps

**Applies to:** every Valley Christian Startup Incubator app hosted on the VCAI
Mac Studio (valleychristianai.com).
**Short version:** branch off `main`, open a pull request, wait for review and
testing, and let the merge deploy the app.

Each app's repository may add its own setup steps. When it does, follow those
too. Examples below that name a specific app are labeled.

## 1. Get the code

1. Get access to the app's private repository in the incubator organization.
2. Clone it and start from the latest `main` branch:

```bash
git clone https://github.com/Valley-Christian-Startup-Incubator/<app-repo>.git
cd <app-repo>
git checkout main
git pull
```

3. Create your own branch named after the feature, like `vocab-speed-round`:

```bash
git checkout -b your-branch-name
```

Never commit straight to `main`. On apps with automatic deployment, merging to
`main` puts the change on the live site.

## 2. Run it on your computer

Copy the app's example environment file and use local-testing values:

```bash
cp .env.example .env
```

- Use development settings and local test data only.
- Never put production keys, passwords, or a copy of the live database on your
  computer. You do not need them to work on the app.
- If the app encrypts personal data, leave its live key alone. Use a fresh key
  only for an empty local database, or leave it blank if the app allows that.

*Example (273Kelvin only):* `PUBLIC_BASE_URL=http://127.0.0.1:8795`,
`PORT=8795`, a long random `SESSION_SECRET`, and
`DEV_LOGIN_EMAIL=you@warriorlife.net` to sign in at `/auth/dev-login` without
Google. Leave `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `AI_API_KEY`, and the
live `NAME_KEY` out of your copy. Start it with `node server.mjs` and run tests
with `node --test test/unit.test.mjs`.

## 3. What never goes in Git

Do **not** commit:

- `.env` files or any other secrets
- encryption keys or key files (`PII_KEY`, or the app's own name for it)
- databases (`data/`, `*.db`, `*.sqlite`) or database exports
- backups, logs, or `node_modules`

If Git offers to commit any of these, stop and unstage them. New features that
store personal data must follow the [PII encryption standard](pii-encryption.md).

## 4. Open a pull request

1. Commit on your branch (`git add` the files you changed, then `git commit`).
2. Push the branch: `git push -u origin your-branch-name`.
3. On GitHub, open a **pull request into `main`**.
4. Mr. Mull will review it. Please wait for that review. Do not merge it yourself
   unless you have been asked to.

## 5. Review and testing

The reviewer:

1. Reads the changes.
2. Runs the branch on the shared test site,
   [test.valleychristianai.com](https://test.valleychristianai.com), using a copy
   of the app's database, never the live database.
3. Merges into `main` after the change works there.

The test address points at whichever app is under review, so only one pull
request is tested there at a time.

## 6. What happens after a merge

On apps that use [automatic deployment](skills/big-mac-autodeploy/SKILL.md), the
Studio deploys the merged `main` in about **five minutes**. Do not upload files
or edit the live copy on the Studio by hand.

To check the live site, open it, sign in, and use the app's health URL if it has
one (*example, 273Kelvin:* `/health`).

If something looks wrong after a deploy, tell Mr. Mull (bmull@vcs.net) before
trying to fix it live. Rolling back is done from Git, not by editing files on
the server.
