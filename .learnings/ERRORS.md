# Errors

Command failures and integration errors.

---

## [ERR-20260908-001] bws-run-git-fetch

**Logged**: 2026-09-08T00:00:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
`bws run` could not start the authenticated Git fetch because no access token is available to the CLI.

### Error
`Missing access token`

### Context
- Attempted: `bws run -- git fetch --prune origin`.
- The process environment has no `BWS_ACCESS_TOKEN` and the default BWS config file is absent.
- No Git remote operation or repository change occurred.

### Suggested Fix
Provide the Bitwarden Secrets access token to the current session through the approved local secret mechanism, then retry the fetch, rebase, validation, and push sequence.

### Metadata
- Reproducible: yes
- Related Files: none

---

### Resolution
- **Resolved**: 2026-09-08T00:00:00Z
- **Notes**: The access token was supplied from the approved local secret file. BWS started normally; a separate network failure now blocks GitHub access.

---

## [ERR-20260908-002] bws-run-git-fetch-network

**Logged**: 2026-09-08T00:00:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
The GitHub fetch initiated through `bws run` could not establish an HTTPS connection.

### Error
`Failed to connect to github.com port 443`

### Context
- BWS accepted the locally supplied access token and started the command.
- `git fetch --prune origin` failed before remote authentication or data transfer.
- No remote or repository state changed.

### Suggested Fix
Restore HTTPS connectivity to GitHub in this WSL environment, then retry the fetch, rebase, validation, and push sequence.

### Metadata
- Reproducible: yes
- Related Files: none

---

## [ERR-20260903-001] temporary-test-cleanup

**Logged**: 2026-09-03T00:00:00Z
**Priority**: low
**Status**: resolved
**Area**: tests

### Summary
The environment rejected direct recursive removal of the isolated notesmd-cli test directory.

### Error
The command policy rejected `rm -rf` before it ran.

### Context
- The directory was created for an isolated CLI test under `/tmp`.
- No test files were removed by the rejected command.

### Suggested Fix
Use a recoverable move when cleanup is needed, or leave the short-lived temporary directory for the system to purge.

### Metadata
- Reproducible: yes
- Related Files: none

### Resolution
- **Resolved**: 2026-09-03T00:00:00Z
- **Notes**: The directory contains only disposable test files and is left for normal temporary-file cleanup.

---
