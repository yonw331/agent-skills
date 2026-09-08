import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def run_validator(self, text):
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "demo"
            skill.mkdir()
            if text is not None:
                (skill / "SKILL.md").write_bytes(text.encode("utf-8"))
            return subprocess.run(
                ["bash", str(ROOT / "scripts/validate-skill.sh"), str(skill)],
                text=True, capture_output=True, check=False,
            )

    def test_valid_extensions_and_multiline_description(self):
        result = self.run_validator(
            "---\nname: demo\ndescription: |-\n  first\n  second\n"
            "tools: [read, exec]\nmetadata:\n  version: 1\n---\n# Body\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_crlf(self):
        self.assertEqual(self.run_validator(
            "---\r\nname: demo\r\ndescription: ok\r\n---\r\n"
        ).returncode, 0)

    def test_bom(self):
        self.assertEqual(self.run_validator(
            "\ufeff---\nname: demo\ndescription: ok\n---\n"
        ).returncode, 0)

    def test_invalid_yaml(self):
        result = self.run_validator(
            '---\nname: demo\ndescription: ok\nsummary: "ok"\n  stray text\n---\n'
        )
        self.assertNotEqual(result.returncode, 0)

    def test_invalid_tools_indentation(self):
        self.assertNotEqual(self.run_validator(
            "---\nname: demo\ndescription: ok\ntools:\n  - - read\n- exec\n---\n"
        ).returncode, 0)

    def test_body_fields_do_not_satisfy_frontmatter(self):
        self.assertNotEqual(self.run_validator(
            "---\nmetadata: {}\n---\nname: demo\ndescription: body only\n"
        ).returncode, 0)

    def test_missing_closing_delimiter(self):
        self.assertNotEqual(self.run_validator(
            "---\nname: demo\ndescription: ok\n"
        ).returncode, 0)

    def test_indented_delimiter_is_not_frontmatter(self):
        self.assertNotEqual(self.run_validator(
            "  ---\nname: demo\ndescription: ok\n---\n"
        ).returncode, 0)

    def test_duplicate_keys(self):
        self.assertNotEqual(self.run_validator(
            "---\nname: demo\nname: other\ndescription: ok\n---\n"
        ).returncode, 0)

    def test_non_mapping(self):
        self.assertNotEqual(self.run_validator("---\n- item\n---\n").returncode, 0)

    def test_empty_and_non_string_fields(self):
        for value in ["null", "true", "123", "[]", "'   '"]:
            with self.subTest(value=value):
                self.assertNotEqual(self.run_validator(
                    f"---\nname: demo\ndescription: {value}\n---\n"
                ).returncode, 0)

    def test_missing_file(self):
        self.assertNotEqual(self.run_validator(None).returncode, 0)

    def test_unsafe_yaml_and_error_redaction(self):
        result = self.run_validator(
            "---\nname: demo\ndescription: !!python/object/apply:os.system "
            "['UNTRUSTED_FIXTURE_DO_NOT_ECHO']\n---\n"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("UNTRUSTED_FIXTURE_DO_NOT_ECHO", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
