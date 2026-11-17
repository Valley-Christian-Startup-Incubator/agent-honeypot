# Secret

Private notes for agents working on `valley-big-mac`. Git ignores everything
in this folder except this README and `.gitignore`, so its notes never reach
the public repository.

The files exist only in the Studio's checkout. Copy a new note there with
`scp` instead of committing it. Notes may name file paths and variable names,
but never credential values.

## Files

- `pii-keys.md`: where each encrypted app keeps its PII keys. See the
  [PII encryption standard](../pii-encryption.md).
