#!/usr/bin/env python3
"""Validate the structural contract of a test requirements document."""

from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "## 1. 一页读懂",
    "## 2. 功能如何运作",
    "## 3. 范围",
    "## 4. 业务规则",
    "## 5. 状态与阶段流转",
    "## 6. 数据影响",
    "## 7. 异常与边界",
    "## 8. 核心验收点",
    "## 9. 待确认事项",
    "## 10. 推断项",
    "## 附录 A：测试相关技术证据",
    "## 附录 B：需求追溯摘要",
)

IDENTIFIER_PATTERNS = {
    "BR": re.compile(r"\bBR-(\d{2,3})\b"),
    "AB": re.compile(r"\bAB-(\d{2,3})\b"),
    "AC": re.compile(r"\bAC-(\d{2,3})\b"),
}

DOCUMENT_SCHEMA = "tdtr/v1"

SECTION_BOUNDS = {
    "BR": ("## 4. 业务规则", "## 5. 状态与阶段流转"),
    "AB": ("## 7. 异常与边界", "## 8. 核心验收点"),
    "AC": ("## 8. 核心验收点", "## 9. 待确认事项"),
}

DEFINITION_PATTERNS = {
    prefix: re.compile(rf"^\|\s*{prefix}-(\d{{2,3}})\s*\|", re.MULTILINE)
    for prefix in IDENTIFIER_PATTERNS
}

TECHNICAL_TOKENS = re.compile(
    r"\b(?:[A-Za-z][A-Za-z0-9]*(?:Controller|ServiceImpl|Handler|Dto|DTO|Mapper|Engine|Builder))\b"
    r"|\b[A-Za-z][A-Za-z0-9]*\.[A-Za-z][A-Za-z0-9]*\b"
    r"|\b(?:SELECT|INSERT|UPDATE|DELETE|ALTER TABLE|CREATE TABLE)\b",
    re.IGNORECASE,
)

UNRESOLVED_AC = re.compile(
    r"待确认|最终确认|按.{0,12}(?:策略|方案|口径)(?:处理|执行|为准|决定)"
    r"|失败[、/或]+处理中|处理中[、/或]+待补偿|失败[、/或]+待补偿"
)

STANDALONE_PLACEHOLDER = re.compile(
    r"(?m)(?:^\s*|^\s*-\s+|\|\s*)\{[^{}\n]+\}(?=\s*(?:\||$))"
)
KNOWN_INLINE_PLACEHOLDER = re.compile(
    r"\{[^{}\n]*(?:功能名|业务痛点|解决方案|使用时机|成功结果|范围内能力|"
    r"非目标|保持原行为|业务动作|系统行为|条件或异常|可观察结果|上下文依据|"
    r"author|date|project_tag|source_doc)[^{}\n]*\}"
)
IDENTIFIER_RANGE = re.compile(
    r"\b(BR|AB|AC)-(\d{2,3})\s*[～~]\s*(?:(BR|AB|AC)-)?(\d{2,3})\b"
)


def section(content: str, start: str, end: str | None) -> str:
    start_at = content.find(start)
    if start_at < 0:
        return ""
    end_at = content.find(end, start_at + len(start)) if end else -1
    return content[start_at:] if end_at < 0 else content[start_at:end_at]


def extract_identifiers(content: str) -> set[str]:
    identifiers = {
        match.group(0)
        for pattern in IDENTIFIER_PATTERNS.values()
        for match in pattern.finditer(content)
    }
    for match in IDENTIFIER_RANGE.finditer(content):
        start_prefix, start_value, end_prefix, end_value = match.groups()
        if end_prefix and end_prefix != start_prefix:
            continue
        start_number = int(start_value)
        end_number = int(end_value)
        if start_number <= end_number and end_number - start_number <= 999:
            identifiers.update(
                f"{start_prefix}-{number:02d}"
                for number in range(start_number, end_number + 1)
            )
    return identifiers


def frontmatter(content: str) -> dict[str, str] | None:
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if not match:
        return None

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if field:
            fields[field.group(1)] = field.group(2).strip().strip('"')
    return fields


def definition_numbers(content: str, prefix: str) -> list[int]:
    start, end = SECTION_BOUNDS[prefix]
    values = DEFINITION_PATTERNS[prefix].findall(section(content, start, end))
    return [int(value) for value in values]


def validate_sequence(content: str, prefix: str, errors: list[str]) -> None:
    numbers = definition_numbers(content, prefix)
    if not numbers:
        errors.append(f"missing {prefix} identifiers")
        return

    duplicates = sorted(number for number, count in Counter(numbers).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate {prefix} identifiers: {duplicates}")

    unique = sorted(set(numbers))
    expected = list(range(1, unique[-1] + 1))
    if unique != expected:
        errors.append(f"{prefix} identifiers are not continuous: found {unique}, expected {expected}")


def validate_headings(content: str, errors: list[str]) -> None:
    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        matches = list(re.finditer(rf"^{re.escape(heading)}$", content, re.MULTILINE))
        if not matches:
            errors.append(f"missing heading: {heading}")
            continue
        if len(matches) > 1:
            errors.append(f"duplicate heading: {heading}")
        positions.append(matches[0].start())
    if len(positions) == len(REQUIRED_HEADINGS) and positions != sorted(positions):
        errors.append("required headings are out of order")


def validate_marker_summary(
    content: str,
    marker: str,
    summary_start: str,
    summary_end: str,
    errors: list[str],
) -> None:
    summary = section(content, summary_start, summary_end)
    outside = content.replace(summary, "", 1)
    marked_ids = {
        requirement
        for line in outside.splitlines()
        if marker in line
        for requirement in extract_identifiers(line)
        if requirement.startswith(("BR-", "AB-"))
    }
    missing = sorted(requirement for requirement in marked_ids if requirement not in summary)
    if missing:
        errors.append(f"{marker} requirements missing from summary: {', '.join(missing)}")
    if marker in outside and marker not in summary:
        errors.append(f"document contains {marker} markers but no matching summary")


def validate(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []

    metadata = frontmatter(content)
    if metadata is None:
        errors.append("missing YAML frontmatter")
        metadata = {}

    for field, expected in (
        ("status", "ongoing"),
        ("review_status", None),
        ("source", None),
        ("document_schema", DOCUMENT_SCHEMA),
    ):
        value = metadata.get(field, "")
        if not value:
            errors.append(f"missing frontmatter field: {field}")
        elif expected and value != expected:
            errors.append(f"frontmatter {field} must be {expected}")

    if metadata.get("review_status") not in {None, "", "draft", "reviewed"}:
        errors.append("frontmatter review_status must be draft or reviewed")
    if metadata.get("review_status") == "reviewed":
        for field in ("reviewed", "reviewer"):
            if not metadata.get(field):
                errors.append(f"reviewed document is missing frontmatter field: {field}")

    validate_headings(content, errors)

    if not path.name.startswith("test-req-"):
        errors.append("filename must start with test-req-")

    for prefix in IDENTIFIER_PATTERNS:
        validate_sequence(content, prefix, errors)

    placeholders = sorted(
        set(KNOWN_INLINE_PLACEHOLDER.findall(content))
        | {match.group(0).strip() for match in STANDALONE_PLACEHOLDER.finditer(content)}
    )
    if placeholders:
        errors.append("unresolved template placeholders: " + ", ".join(placeholders[:10]))

    understanding = section(content, "## 1. 一页读懂", "## 3. 范围")
    leaked = sorted(set(match.group(0) for match in TECHNICAL_TOKENS.finditer(understanding)))
    if leaked:
        errors.append("technical identifiers leaked into understanding layer: " + ", ".join(leaked[:10]))

    validate_marker_summary(content, "🚧", "## 9. 待确认事项", "## 10. 推断项", errors)
    validate_marker_summary(content, "📌", "## 10. 推断项", "## 附录 A：测试相关技术证据", errors)

    known_by_prefix = {
        prefix: {f"{prefix}-{number:02d}" for number in definition_numbers(content, prefix)}
        for prefix in IDENTIFIER_PATTERNS
    }
    known_requirements = known_by_prefix["BR"] | known_by_prefix["AB"]
    all_known_identifiers = set().union(*known_by_prefix.values())
    referenced_identifiers = {
        identifier
        for identifier in extract_identifiers(content)
        if identifier not in all_known_identifiers
    }
    if referenced_identifiers:
        errors.append("references unknown identifiers: " + ", ".join(sorted(referenced_identifiers)))

    ac_section = section(content, "## 8. 核心验收点", "## 9. 待确认事项")
    has_end_to_end_ac = False
    for line in ac_section.splitlines():
        if "| AC-" not in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and "端到端" in cells[1] and "正常" in cells[1]:
            has_end_to_end_ac = True
        if len(cells) < 5 or not cells[3] or cells[3] in {"-", "待确认", "{页面、任务、数据或外部结果}"}:
            errors.append(f"acceptance criterion has no observable result: {line.strip()}")
        elif UNRESOLVED_AC.search(cells[3]):
            errors.append(f"acceptance criterion depends on an unresolved or multi-option result: {line.strip()}")
        refs = set(re.findall(r"\b(?:BR|AB)-\d{2,3}\b", line))
        if not refs:
            errors.append(f"acceptance criterion has no BR/AB reference: {line.strip()}")
        invalid = sorted(refs - known_requirements)
        if invalid:
            errors.append(f"acceptance criterion references unknown requirements: {', '.join(invalid)}")

    if not has_end_to_end_ac:
        errors.append("missing an acceptance criterion labeled as an end-to-end normal flow")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    args = parser.parse_args()

    if not args.document.is_file():
        print(f"ERROR: file not found: {args.document}", file=sys.stderr)
        return 2

    errors = validate(args.document)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {args.document}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
