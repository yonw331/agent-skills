"""Read YAML frontmatter safely, retaining community extension fields."""
from pathlib import Path

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in result
            except TypeError:
                raise ValueError("invalid YAML mapping key") from None
            if duplicate:
                raise ValueError("duplicate YAML key")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def parse_frontmatter(content):
    lines = content.lstrip("\ufeff").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening frontmatter delimiter")
    end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
    if end is None:
        raise ValueError("missing closing frontmatter delimiter")
    try:
        metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        location = f" at line {mark.line + 2}, column {mark.column + 1}" if mark else ""
        raise ValueError(f"invalid YAML{location}") from None
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a mapping")
    for field in ("name", "description"):
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a nonempty frontmatter string")
    return metadata


def read_skill(path):
    try:
        return parse_frontmatter(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError) as error:
        raise ValueError(f"cannot read skill: {type(error).__name__}") from None


def skill_entrypoints(root):
    """Stop at a skill package; nested files belong to that package."""
    for directory in sorted(Path(root).iterdir()):
        if not directory.is_dir():
            continue
        entrypoint = directory / "SKILL.md"
        if entrypoint.is_file():
            yield entrypoint
        else:
            yield from skill_entrypoints(directory)
