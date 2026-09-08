import json
import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProvenanceTests(unittest.TestCase):
    def test_python_testing_matches_locked_source(self):
        lock = json.loads((ROOT / "community/source-lock.json").read_text())
        source = lock["sources"]["Luohaothu/everything-codex:python-testing"]
        content = (ROOT / source["path"] / "SKILL.md").read_bytes()
        expected = source["files"]["SKILL.md"]
        self.assertEqual(len(content), expected["bytes"])
        self.assertEqual(hashlib.sha256(content).hexdigest(), expected["sha256"])
        self.assertRegex(source["revision"], r"^[0-9a-f]{40}$")


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "scripts", self.root / "scripts",
                        ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "curated").mkdir()
        (self.root / "community").mkdir()

    def skill(self, relative, text):
        target = self.root / relative / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def command(self, script):
        return subprocess.run(["bash", str(self.root / "scripts" / script)],
                              capture_output=True, text=True, check=False)

    def test_grouped_package_boundary_and_description(self):
        self.skill("community/group/demo",
                   "---\nname: demo\ndescription: >-\n  first\n  second\n---\n")
        self.skill("community/group/demo/reference", "# Supporting document\n")
        self.assertEqual(self.command("validate-skill.sh").returncode, 0)
        result = self.command("build-registry.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads((self.root / "registry.json").read_text())["skills"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["path"], "community/group/demo/")
        self.assertEqual(entries[0]["description"], "first second")
        self.assertIn("first second", (self.root / "SKILLS.md").read_text())

    def test_invalid_skill_preserves_existing_outputs(self):
        self.skill("curated/demo", "---\nname: demo\n---\ndescription: body\n")
        for filename in ("registry.json", "SKILLS.md"):
            (self.root / filename).write_text("existing output")
        self.assertNotEqual(self.command("build-registry.sh").returncode, 0)
        for filename in ("registry.json", "SKILLS.md"):
            self.assertEqual((self.root / filename).read_text(), "existing output")

    def test_full_scan_reports_multiple_errors(self):
        self.skill("curated/one", "---\nname: one\ndescription: null\n---\n")
        self.skill("community/group/two", "no frontmatter")
        result = self.command("validate-skill.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("errors: 2", result.stdout)

    def test_empty_validation_is_not_success(self):
        self.assertNotEqual(self.command("validate-skill.sh").returncode, 0)

    def test_invalid_utf8_is_reported_without_traceback(self):
        self.skill("curated/demo", "")
        (self.root / "curated/demo/SKILL.md").write_bytes(b"\xff")
        result = self.command("validate-skill.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
