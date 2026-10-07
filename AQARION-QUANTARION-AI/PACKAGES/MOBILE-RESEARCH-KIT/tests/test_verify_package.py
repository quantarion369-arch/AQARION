import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


TOOL = Path(__file__).resolve().parents[1] / "tools" / "verify_package.py"
SPEC = importlib.util.spec_from_file_location("package_verifier_under_test", TOOL)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class VerifyPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "package"
        self.root.mkdir()
        self.content = b"original content"
        (self.root / "sample.txt").write_bytes(self.content)
        self.entry = {
            "path": "sample.txt",
            "bytes": len(self.content),
            "sha256": hashlib.sha256(self.content).hexdigest(),
        }
        self.write_manifest([self.entry])

    def write_manifest(self, entries, algorithm="sha256"):
        data = {"algorithm": algorithm, "files": entries}
        (self.root / "manifest.json").write_text(
            json.dumps(data), encoding="utf-8"
        )

    def run_verifier(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = verifier.main(["--root", str(self.root)])
        return code, output.getvalue()

    def test_matching_file_passes(self):
        code, output = self.run_verifier()
        self.assertEqual(code, 0)
        self.assertIn("PACKAGE_VERIFICATION_OK", output)

    def test_same_size_changed_content_fails(self):
        (self.root / "sample.txt").write_bytes(b"X" * len(self.content))
        code, output = self.run_verifier()
        self.assertEqual(code, 1)
        self.assertIn("SHA-256 mismatch", output)

    def test_wrong_recorded_size_fails(self):
        self.write_manifest([dict(self.entry, bytes=999)])
        code, output = self.run_verifier()
        self.assertEqual(code, 1)
        self.assertIn("bytes expected", output)

    def test_missing_file_fails(self):
        (self.root / "sample.txt").unlink()
        code, output = self.run_verifier()
        self.assertEqual(code, 1)
        self.assertIn("Missing file", output)

    def test_directory_instead_of_file_fails(self):
        (self.root / "sample.txt").unlink()
        (self.root / "sample.txt").mkdir()
        code, output = self.run_verifier()
        self.assertEqual(code, 1)
        self.assertIn("not a regular file", output)

    def test_duplicate_paths_rejected(self):
        self.write_manifest([self.entry, self.entry])
        code, output = self.run_verifier()
        self.assertEqual(code, 2)
        self.assertIn("Duplicate file path", output)

    def test_unsafe_paths_rejected(self):
        paths = [
            "../outside.txt",
            "/outside.txt",
            "folder/../sample.txt",
            "./sample.txt",
            "folder//sample.txt",
            "folder/",
            "C:/sample.txt",
            "folder" + chr(92) + "sample.txt",
        ]
        for name in paths:
            with self.subTest(path=name):
                self.write_manifest([dict(self.entry, path=name)])
                code, output = self.run_verifier()
                self.assertEqual(code, 2)
                self.assertIn("unsafe path", output)

    def test_invalid_sizes_rejected(self):
        for size in (True, -1, 1.5, "16", None):
            with self.subTest(size=size):
                self.write_manifest([dict(self.entry, bytes=size)])
                code, output = self.run_verifier()
                self.assertEqual(code, 2)
                self.assertIn("invalid byte size", output)

    def test_invalid_hash_rejected(self):
        self.write_manifest([dict(self.entry, sha256="not-a-hash")])
        code, output = self.run_verifier()
        self.assertEqual(code, 2)
        self.assertIn("invalid SHA-256", output)

    def test_wrong_algorithm_rejected(self):
        self.write_manifest([self.entry], algorithm="md5")
        code, output = self.run_verifier()
        self.assertEqual(code, 2)
        self.assertIn("algorithm must be sha256", output)

    def test_empty_file_list_rejected(self):
        self.write_manifest([])
        code, output = self.run_verifier()
        self.assertEqual(code, 2)
        self.assertIn("nonempty list", output)

    def test_malformed_json_rejected(self):
        (self.root / "manifest.json").write_text("{", encoding="utf-8")
        code, output = self.run_verifier()
        self.assertEqual(code, 2)
        self.assertIn("MANIFEST_ERROR", output)

    def test_duplicate_json_key_rejected(self):
        text = '{"algorithm":"sha256","algorithm":"sha256","files":[]}'
        (self.root / "manifest.json").write_text(text, encoding="utf-8")
        code, output = self.run_verifier()
        self.assertEqual(code, 2)
        self.assertIn("Duplicate JSON key", output)

    def test_unlisted_file_does_not_change_result(self):
        (self.root / "extra.txt").write_bytes(b"unlisted")
        code, output = self.run_verifier()
        self.assertEqual(code, 0)
        self.assertIn("unlisted files are not verified", output)

    def test_uppercase_hash_accepted(self):
        self.write_manifest([
            dict(self.entry, sha256=self.entry["sha256"].upper())
        ])
        code, output = self.run_verifier()
        self.assertEqual(code, 0)

    def test_symlink_rejected(self):
        target = self.root / "sample.txt"
        link = self.root / "linked.txt"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            self.skipTest("Symlinks unavailable: " + str(exc))
        self.write_manifest([dict(self.entry, path="linked.txt")])
        code, output = self.run_verifier()
        self.assertEqual(code, 1)
        self.assertIn("Symbolic links are not permitted", output)


if __name__ == "__main__":
    unittest.main()
