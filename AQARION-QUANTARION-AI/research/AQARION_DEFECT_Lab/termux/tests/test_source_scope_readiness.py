import os
import unittest
from pathlib import Path

FILES = ("api.py", "retrieve.py", "context.py", "corpus/MANIFEST.md")

class SourceScopeReadinessTests(unittest.TestCase):
    def setUp(self):
        value = os.environ.get("AQARION_RAG_PATH")
        if not value:
            self.skipTest("AQARION_RAG_PATH not set")
        self.root = Path(value).expanduser().resolve()

    def test_required_files_exist(self):
        missing = [f for f in FILES if not (self.root / f).is_file()]
        self.assertEqual(missing, [], f"missing files: {missing}")

    def test_source_scope_surface(self):
        api = (self.root / "api.py").read_text(encoding="utf-8")
        retrieve = (self.root / "retrieve.py").read_text(encoding="utf-8")
        context = (self.root / "context.py").read_text(encoding="utf-8")
        indicators = {
            "api source_id": "source_id" in api,
            "resolver": (
                "resolve_source_id" in retrieve
                or "resolve_pinned_source" in retrieve
            ),
            "retrieval source_id": "source_id" in retrieve,
            "context source_id": "source_id" in context,
        }
        print("\nSOURCE SCOPE STATIC READINESS")
        for name, found in indicators.items():
            print(f"{name}={found}")
        self.assertTrue(
            any(indicators.values()),
            "No source-scope indicators found; inspect actual patch state."
        )

if __name__ == "__main__":
    unittest.main()
