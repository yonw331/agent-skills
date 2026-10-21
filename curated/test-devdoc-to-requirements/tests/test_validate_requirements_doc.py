import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "validate_requirements_doc.py"
SPEC = importlib.util.spec_from_file_location("validate_requirements_doc", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def valid_document() -> str:
    return """---
title: 测试需求确认-示例
status: ongoing
review_status: draft
document_schema: tdtr/v1
source: "[[示例设计]]"
---

# 测试需求确认-示例

## 1. 一页读懂

操作员提交业务，系统完成处理并更新任务和业务记录。

## 2. 功能如何运作

操作员发起，系统校验并完成。

## 3. 范围

包含正常处理，不包含外部系统改造。

## 4. 业务规则

| 编号 | 规则 | 来源 |
| --- | --- | --- |
| BR-01 | 条件满足时，系统完成业务并更新记录。 | 原设计 1 |

## 5. 状态与阶段流转

待处理 -> 已完成

## 6. 数据影响

任务由待处理变为已完成。

## 7. 异常与边界

| 编号 | 场景 | 预期 | 来源 |
| --- | --- | --- | --- |
| AB-01 | 如果条件不满足 | 则阻断业务且不更新记录 | 原设计 2 |

## 8. 核心验收点

| 编号 | 覆盖场景 | 前提与动作 | 可观察结果 | 关联需求 |
| --- | --- | --- | --- | --- |
| AC-01 | 端到端正常流程 | 条件满足时提交业务 | 任务完成且业务记录已更新 | BR-01 |
| AC-02 | 条件阻断 | 条件不满足时提交业务 | 业务被阻断且记录未更新 | AB-01 |

## 9. 待确认事项

无。

## 10. 推断项

无。

## 附录 A：测试相关技术证据

无。

## 附录 B：需求追溯摘要

| 需求 | 来源章节 | 验收点 | 状态 |
| --- | --- | --- | --- |
| BR-01 | 原设计 1 | AC-01 | 已确认 |
| AB-01 | 原设计 2 | AC-02 | 已确认 |
"""


class RequirementsValidatorTest(unittest.TestCase):
    def validate(self, content: str) -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test-req-example.md"
            path.write_text(content, encoding="utf-8")
            return MODULE.validate(path)

    def assert_has_error(self, content: str, expected: str) -> None:
        errors = self.validate(content)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_accepts_valid_document(self):
        self.assertEqual([], self.validate(valid_document()))

    def test_rejects_duplicate_identifier(self):
        content = valid_document().replace(
            "| BR-01 | 条件满足时，系统完成业务并更新记录。 | 原设计 1 |",
            "| BR-01 | 条件满足时，系统完成业务并更新记录。 | 原设计 1 |\n"
            "| BR-01 | 重复规则。 | 原设计 1 |",
        )
        self.assert_has_error(content, "duplicate BR identifiers")

    def test_rejects_unresolved_template_placeholder(self):
        content = valid_document().replace("操作员提交业务", "{业务痛点、解决方案}")
        self.assert_has_error(content, "unresolved template placeholders")

    def test_rejects_unknown_identifier_outside_acceptance_criteria(self):
        content = valid_document().replace(
            "| AB-01 | 原设计 2 | AC-02 | 已确认 |",
            "| AB-01～AB-03 | 原设计 2 | AC-02 | 已确认 |",
        )
        errors = self.validate(content)
        self.assertTrue(any("AB-02" in error for error in errors), errors)
        self.assertTrue(any("AB-03" in error for error in errors), errors)

    def test_rejects_marked_requirement_missing_from_summary(self):
        content = valid_document().replace(
            "| BR-01 | 条件满足时，系统完成业务并更新记录。 | 原设计 1 |",
            "| BR-01 | 条件满足时，系统完成业务并更新记录。 | 🚧 原设计 1 |",
        )
        self.assert_has_error(content, "BR-01")

    def test_rejects_missing_document_schema(self):
        content = valid_document().replace("document_schema: tdtr/v1\n", "")
        self.assert_has_error(content, "document_schema")

    def test_reviewed_document_requires_review_metadata(self):
        content = valid_document().replace("review_status: draft", "review_status: reviewed")
        errors = self.validate(content)
        self.assertTrue(any("reviewed" in error for error in errors), errors)
        self.assertTrue(any("reviewer" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
