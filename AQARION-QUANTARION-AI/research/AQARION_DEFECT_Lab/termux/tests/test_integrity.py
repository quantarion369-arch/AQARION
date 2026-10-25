import hashlib
import unittest

class IntegrityTests(unittest.TestCase):
    def test_hash_determinism(self):
        data = b"pinned source text\n"
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            hashlib.sha256(data).hexdigest(),
        )

    def test_half_open_offsets(self):
        text = "abcDEFghi"
        start, end = 3, 6
        self.assertEqual(text[start:end], "DEF")
        self.assertEqual(end - start, len(text[start:end]))

if __name__ == "__main__":
    unittest.main()
