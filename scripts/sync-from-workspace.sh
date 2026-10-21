#!/bin/bash
# Sync missing workspace skills into this repository without replacing snapshots.
# Usage: ./scripts/sync-from-workspace.sh <workspace-skills-dir> [--global-dir <dir>]

set -euo pipefail

WORKSPACE_SKILLS="${1:-}"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
GLOBAL_DIR=""

usage() {
  echo "Usage: $0 <workspace-skills-dir> [--global-dir <dir>]"
}

if [ -z "$WORKSPACE_SKILLS" ]; then
  usage
  exit 1
fi
shift

while [ "$#" -gt 0 ]; do
  case "$1" in
    --global-dir)
      [ "$#" -ge 2 ] || { echo "Error: --global-dir requires a directory"; exit 1; }
      GLOBAL_DIR="$2"
      shift 2
      ;;
    *)
      echo "Error: unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

[ -d "$WORKSPACE_SKILLS" ] || { echo "Error: source directory does not exist: $WORKSPACE_SKILLS"; exit 1; }
[ -z "$GLOBAL_DIR" ] || [ -d "$GLOBAL_DIR" ] || { echo "Error: global directory does not exist: $GLOBAL_DIR"; exit 1; }

is_community() {
  [ -f "$1/_meta.json" ] || [ -f "$1/.clawhub/origin.json" ]
}

normalize_entrypoint() {
  local skill_dir="$1"
  if [ -f "$skill_dir/skill.md" ] && [ ! -e "$skill_dir/SKILL.md" ]; then
    mv "$skill_dir/skill.md" "$skill_dir/SKILL.md"
    echo "    normalized entrypoint: skill.md -> SKILL.md"
  fi
}

compare_skill() {
  local source="$1" target="$2" label="$3"
  if diff -qr --exclude=SKILL.md "$source" "$target" >/dev/null 2>&1; then
    if [ -f "$source/SKILL.md" ] && [ -f "$target/SKILL.md" ] && cmp -s "$source/SKILL.md" "$target/SKILL.md"; then
      echo "  existing $label: identical"
    else
      echo "  existing $label: differs (preserved)"
    fi
  else
    echo "  existing $label: differs (preserved)"
  fi
}

echo "=== Sync workspace skills ==="
echo "Source: $WORKSPACE_SKILLS"
echo "Repository: $REPO_DIR"
[ -z "$GLOBAL_DIR" ] || echo "Global directory: $GLOBAL_DIR"

synced=0
preserved=0
global_installed=0
global_preserved=0

for source in "$WORKSPACE_SKILLS"/*/; do
  [ -d "$source" ] || continue
  name="$(basename "$source")"
  section="curated"
  is_community "$source" && section="community"
  target="$REPO_DIR/$section/$name"

  if [ -e "$target" ] || [ -L "$target" ]; then
    compare_skill "$source" "$target" "$section/$name"
    preserved=$((preserved + 1))
  else
    cp -a "$source" "$target"
    normalize_entrypoint "$target"
    echo "  added $section/$name"
    synced=$((synced + 1))
  fi

  [ -z "$GLOBAL_DIR" ] && continue
  global_target="$GLOBAL_DIR/$name"
  if [ -e "$global_target" ] || [ -L "$global_target" ]; then
    compare_skill "$target" "$global_target" "global/$name"
    global_preserved=$((global_preserved + 1))
  else
    cp -a "$target" "$global_target"
    echo "  installed global/$name"
    global_installed=$((global_installed + 1))
  fi
done

echo "=== Complete: added=$synced, repository-existing=$preserved, global-installed=$global_installed, global-existing=$global_preserved ==="
