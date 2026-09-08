#!/bin/bash
# Keep the public CLI while Python handles YAML parsing and diagnostics.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$REPO_DIR/scripts/validate_skill.py" "$@"
