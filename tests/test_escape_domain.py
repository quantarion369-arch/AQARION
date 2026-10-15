import unittest

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

PATH = (
    Path(__file__).resolve().parents[1]
    / "AQARION-QUANTARION-AI"
    / "PACKAGES"
    / "AQARION-RAG"
    / "assess.py"
)
SPEC = spec_from_file_location("aqarion_assess", PATH)
ASSESS = module_from_spec(SPEC)
SPEC.loader.exec_module(ASSESS)


class EscapeDomainTests(unittest.TestCase):
    def test_parameter_above_two_escapes(self):
        self.assertFalse(ASSESS.stable_bounded_orbit(2.01))

    def test_parameter_below_minus_two_escapes(self):
        self.assertFalse(ASSESS.stable_bounded_orbit(-2.01))

    def test_boundary_minus_two_does_not_trigger_strict_threshold(self):
        self.assertTrue(ASSESS.stable_bounded_orbit(-2.0))

    def test_zero_iterations_is_no_escape_observed(self):
        self.assertTrue(ASSESS.stable_bounded_orbit(100.0, iters=0))

    def test_negative_iteration_count_rejected(self):
        with self.assertRaises(ValueError):
            ASSESS.stable_bounded_orbit(0.0, iters=-1)


if __name__ == "__main__":
    unittest.main()
