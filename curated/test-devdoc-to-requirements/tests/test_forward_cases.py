import json
import os
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).parents[1]
CASES_PATH = Path(__file__).with_name("forward-cases.json")


def load_cases():
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def find_corpus_root(cases):
    configured = os.environ.get("TDTR_FORWARD_CORPUS_ROOT")
    candidates = ([Path(configured)] if configured else []) + list(SKILL_DIR.parents)
    for candidate in candidates:
        if all((candidate / case["source"]).is_file() for case in cases):
            return candidate
    return None


class ForwardCasesTest(unittest.TestCase):
    def test_corpus_has_five_distinct_runnable_cases(self):
        cases = load_cases()

        self.assertGreaterEqual(len(cases), 5)
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        self.assertEqual(len(cases), len({case["class"] for case in cases}))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertGreaterEqual(len(case["must_cover"]), 3)
                self.assertGreaterEqual(len(case["must_not_assert"]), 2)
                self.assertGreaterEqual(len(case["source_anchors"]), 2)
                self.assertTrue(all(item.strip() for item in case["must_cover"]))
                self.assertTrue(all(item.strip() for item in case["must_not_assert"]))

    def test_source_anchors_match_available_corpus(self):
        cases = load_cases()
        corpus_root = find_corpus_root(cases)
        if corpus_root is None:
            self.skipTest("set TDTR_FORWARD_CORPUS_ROOT to validate source anchors")

        for case in cases:
            with self.subTest(case=case["id"]):
                source_path = corpus_root / case["source"]
                source = source_path.read_text(encoding="utf-8")
                for anchor in case["source_anchors"]:
                    self.assertIn(anchor, source)


if __name__ == "__main__":
    unittest.main()
