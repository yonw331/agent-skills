"""Validate a skill entrypoint or all repository skill packages."""
import argparse
from pathlib import Path

from skill_metadata import read_skill, skill_entrypoints


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", nargs="?")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = (
        [Path(args.skill_dir) / "SKILL.md"] if args.skill_dir
        else sorted(path for namespace in ("curated", "community")
                    for path in skill_entrypoints(root / namespace))
    )
    if not paths:
        print("ERROR: no skill entrypoints found")
        return 1
    errors = 0
    for path in paths:
        try:
            read_skill(path)
        except ValueError as error:
            print(f"ERROR {path}: {error}")
            errors += 1
    print(f"Validated {len(paths)} entrypoints; errors: {errors}")
    return int(errors > 0)


if __name__ == "__main__":
    raise SystemExit(main())
