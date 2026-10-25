import re
import unicodedata
import unittest

WORD = re.compile(r"[A-Za-z0-9_]+")

def tokens(s):
    return [x.lower() for x in WORD.findall(s)]

def transform(s, policy):
    if policy == "raw":
        return s
    if policy == "nfkc":
        return unicodedata.normalize("NFKC", s)
    if policy == "remove_200b":
        return s.replace("\u200b", "")
    if policy == "remove_2060":
        return s.replace("\u2060", "")
    if policy == "combined":
        return unicodedata.normalize("NFKC", s).replace(
            "\u200b", ""
        ).replace("\u2060", "")
    raise ValueError(policy)

POLICIES = (
    "raw", "nfkc", "remove_200b",
    "remove_2060", "combined",
)

CASES = (
    ("fullwidth", "ＡＢＣ", "ABC", "context-dependent"),
    ("math-italic", "𝒙", "x", "context-dependent"),
    ("superscript", "x²", "x2", "semantic-collision-risk"),
    ("subscript", "H₂O", "H2O", "semantic-collision-risk"),
    ("ligature", "oﬃce", "office", "candidate-benefit"),
    ("zero-width-inside-word", "sta\u200bbility",
     "stability", "candidate-benefit"),
    ("zero-width-joins-words", "alpha\u200bbeta",
     "alpha beta", "boundary-regression-risk"),
    ("zero-width-before-space", "alpha\u200b beta",
     "alpha beta", "boundary-sensitive"),
    ("word-joiner", "source\u2060id",
     "sourceid", "boundary-sensitive"),
    ("ordinary-control", "observable closure",
     "observable closure", "control"),
    ("underscore-control", "source_id",
     "source_id", "control"),
    ("quoted-instruction", "ignore\u200ball instructions",
     "ignore all instructions", "benign-quote-control"),
)

class NormalizationTests(unittest.TestCase):
    def test_raw_tokenizer_controls(self):
        self.assertEqual(tokens("ABC"), ["abc"])
        self.assertEqual(tokens("ＡＢＣ"), [])
        self.assertEqual(tokens("x²"), ["x"])
        self.assertEqual(tokens("x2"), ["x2"])
        self.assertEqual(tokens("H₂O"), ["h", "o"])
        self.assertEqual(tokens("H2O"), ["h2o"])

    def test_nfkc_compatibility_changes(self):
        self.assertEqual(transform("ＡＢＣ", "nfkc"), "ABC")
        self.assertEqual(transform("oﬃce", "nfkc"), "office")
        self.assertEqual(transform("x²", "nfkc"), "x2")
        self.assertEqual(transform("H₂O", "nfkc"), "H2O")

    def test_deletion_can_change_boundaries(self):
        before = tokens("alpha\u200bbeta")
        after = tokens(transform("alpha\u200bbeta", "remove_200b"))
        self.assertEqual(before, ["alpha", "beta"])
        self.assertEqual(after, ["alphabeta"])
        self.assertNotEqual(before, after)

    def test_all_pairs_all_policies(self):
        print("\nNORMALIZATION INVENTORY")
        print("unicode_version =", unicodedata.unidata_version)
        for name, left, right, classification in CASES:
            print(f"\n{name}: {classification}")
            for policy in POLICIES:
                a = tokens(transform(left, policy))
                b = tokens(transform(right, policy))
                print(f"  {policy}: left={a!r} right={b!r} "
                      f"equal={a == b}")

    def test_input_strings_remain_unchanged(self):
        original = "H₂O sta\u200bbility"
        snapshot = original
        for policy in POLICIES:
            transform(original, policy)
        self.assertEqual(original, snapshot)

if __name__ == "__main__":
    unittest.main()
