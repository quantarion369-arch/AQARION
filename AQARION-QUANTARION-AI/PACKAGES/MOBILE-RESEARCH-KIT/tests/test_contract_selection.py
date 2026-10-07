import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "contract_collision_lab.py"
)
SPEC = importlib.util.spec_from_file_location(
    "contract_selection_under_test", SOURCE
)
LAB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAB)


class ContractSelectionTests(unittest.TestCase):
    def test_unknown_names_are_rejected_before_execution(self):
        for contract in ("equal", "Parity", "", "unknown"):
            with self.subTest(contract=contract):
                candidate = Mock(return_value=0)

                with self.assertRaisesRegex(
                    ValueError, "Unknown contract:"
                ):
                    LAB.check_contract(
                        candidate, contract, range(-1, 2)
                    )

                candidate.assert_not_called()

    def test_unknown_contract_is_rejected_for_empty_domain(self):
        candidate = Mock(return_value=0)

        with self.assertRaisesRegex(ValueError, "Unknown contract:"):
            LAB.check_contract(candidate, "unknown", [])

        candidate.assert_not_called()

    def test_supported_contracts_remain_distinct(self):
        domain = range(-2, 3)
        equality = LAB.check_contract(
            LAB.subtract_mutation, "equality", domain
        )
        parity = LAB.check_contract(
            LAB.subtract_mutation, "parity", domain
        )

        self.assertFalse(equality["accepted_on_tested_domain"])
        self.assertEqual(equality["inputs_checked"], 1)
        self.assertTrue(parity["accepted_on_tested_domain"])
        self.assertEqual(parity["inputs_checked"], 5)
        self.assertIsNone(parity["first_counterexample"])


if __name__ == "__main__":
    unittest.main()
