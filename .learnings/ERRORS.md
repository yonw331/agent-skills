# Errors

Command failures and integration errors.

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
