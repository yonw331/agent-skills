---
name: bit-secret-manager
description: DISABLED as of 2026-08-31. Do not use for API keys, Tokens, credentials, credential configuration, .env requests, tool authentication, or Bitwarden Secrets Manager access. Never accept secret values in chat.
---

# Bit Secret Manager

> [!warning] Skill disabled
> This Skill and the related manager project are suspended. Do not route
> commands through the manager, initialize profiles, configure credentials,
> install or deploy this Skill, or perform authentication on its behalf.
> Credentials must be handled by the user outside the Agent workflow using a
> currently approved method. Resuming requires explicit re-audit and approval.

`bit-secret-manager` is the execution boundary for local secrets. A schema 2
navigation file stores only profile metadata: BWS Secret IDs and expected keys,
or local logical keys, plus target environment names. BWS values remain in
Bitwarden; local values remain in the device-private store.

## Route (historical; do not execute)

1. Identify the executable and each required environment variable. Classify
   each as `bws` or `local`; IDs, expected keys, logical keys, profile names,
   and environment names are non-secret metadata. Every variable needs one
   mapping in a complete Profile.
2. Find a schema 2 profile in the user's Vault navigation configuration. Do not
   create or edit that shared file automatically. When a mapping is absent,
   stop execution and ask the user to approve adding only source metadata. A
   legacy schema 1 private configuration may be used only with explicit
   `--config`.
3. Have the human initialize a schema 2 file with
   `bit-secret-manager --config /absolute/path/to/config.toml init`. This writes
   only a private device pointer and, when BWS entries exist, obtains a Token by
   hidden input. For a local mapping, have the human run
   `bit-secret-manager set-local LOGICAL_KEY` and enter the value by hidden
   input. Never accept a value or Token in chat, argv, output, notes, logs, or
   shell-sourceable files.
4. Require `bit-secret-manager doctor PROFILE` to pass before a targeted run,
   or use `doctor` for a full-device check. Then execute an argv through the
   profile:

   ```bash
   bit-secret-manager run PROFILE -- executable arg1 arg2
   ```

   Pass arguments separately. Completion means the real operation ran through
   the manager and its exit status was observed.

## Boundaries (historical; do not apply as an active route)

- Convert `.env`, exported-variable, plaintext credential-file, direct `bws`,
  and secret-in-argument requests into execution-time `run` usage. When a tool
  cannot consume inherited environment variables, stop and report that it is
  incompatible with this contract.
- Use a separate read-only BWS Machine Account for each machine that uses BWS.
  Do not claim
  that this removes the accepted risk of a shared high-privilege GitHub PAT.
- `doctor` may report profile, expected-key, and local logical-key names with
  status. Secret values, BWS output, and Token material remain undisclosed.
- The manager installs separately from this skill. Installation never installs
  `bws`, changes shell startup, or creates credentials.
- The executable is `~/.local/bin/bit-secret-manager`; files under
  `~/.local/lib/bit-secret-manager` are implementation files, not commands.
- The private directory is `~/.config/bit-secret-manager/` with `0700`; its
  `device.toml`, `access-token`, and `local-secrets.toml` files are `0600`.

## GitHub

Run `gh api user`, `gh auth setup-git`, and Git operations through the GitHub
profile. `gh auth setup-git` may persist the Git credential helper; keep PATs
out of `gh auth login` and `hosts.yml`.
