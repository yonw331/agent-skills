# agent-skills

This repository owns skill snapshots, source locks, validation and deployment tooling.
For maintenance scope and pending work, read the
[Vault maintenance entry](/mnt/e/wy/400_code/remote/ob-garden/03-Areas/技术成长/系统-技能统一托管.md).
For construction decisions and acceptance evidence, consult the
[archived project](/mnt/e/wy/400_code/remote/ob-garden/05-Archives/Projects/技能统一托管与全局部署/Project.md).

Preserve existing worktree changes. Community adaptations retain upstream provenance
in `community/source-lock.json`. Same-name runtime differences are reported for
manual approval; a source edit does not authorize a global overwrite.

Use the commands documented in README:

```bash
python -m unittest discover -s tests -v
bash scripts/validate-skill.sh
bash scripts/build-registry.sh
```

Install the pinned Python dependency from `scripts/requirements.txt` in an isolated
environment first. Validation must fail on invalid YAML and missing required metadata.
Community extension fields are allowed; package discovery stops at each skill root.

The CI entrypoints are `.github/workflows/validate-skills.yml` and
`.github/workflows/publish-registry.yml`. Offline checks must not run skill business
operations, access credentials or modify live runtime copies. Report local results
separately from remote CI. Commits, pushes and deployment need the user's authority.
