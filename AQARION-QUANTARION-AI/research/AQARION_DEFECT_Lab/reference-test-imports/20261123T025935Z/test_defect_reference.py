import unittest
import numpy as np


def defect_reference(successors, labels):
    """Discrete Koopman defect for an exhaustive finite state set."""
    successors = np.asarray(successors)
    labels = np.asarray(labels)

    if successors.ndim != 1 or labels.ndim != 1:
        raise ValueError("successors and labels must be one-dimensional")

    n = len(successors)
    if n == 0 or len(labels) != n:
        raise ValueError("provide one label and successor per state")

    if not np.issubdtype(successors.dtype, np.integer):
        raise ValueError("successor indices must be integers")

    if np.any(successors < 0) or np.any(successors >= n):
        raise ValueError("successor index outside the state set")

    _, inverse = np.unique(labels, return_inverse=True)
    block_count = int(inverse.max()) + 1

    assignments = np.eye(block_count, dtype=np.float64)[inverse]
    counts = assignments.sum(axis=0)
    projection = (assignments / counts) @ assignments.T

    # (K f)[i] = f[successors[i]]: Koopman pullback convention.
    koopman = np.eye(n, dtype=np.float64)[successors]
    defect = (np.eye(n) - projection) @ koopman @ projection

    return {
        "projection": projection,
        "koopman": koopman,
        "defect": defect,
        "frobenius_squared": float(np.sum(defect * defect)),
        "normalized_loss": float(np.sum(defect * defect) / (n * n)),
        "blocks": block_count,
        "nontrivial_partition": 1 < block_count < n,
    }


class DefectReferenceTests(unittest.TestCase):
    successors = [1, 2, 3, 0]

    def test_closed_partition_has_zero_defect(self):
        result = defect_reference(self.successors, [0, 1, 0, 1])
        np.testing.assert_allclose(
            result["defect"], 0.0, atol=1e-12, rtol=0
        )
        self.assertTrue(result["nontrivial_partition"])

    def test_nonclosed_partition_has_positive_defect(self):
        result = defect_reference(self.successors, [0, 0, 1, 1])
        self.assertGreater(result["frobenius_squared"], 1e-12)

    def test_projection_is_symmetric_and_idempotent(self):
        p = defect_reference(
            self.successors, [0, 0, 1, 1]
        )["projection"]
        np.testing.assert_allclose(p.T, p, atol=1e-12, rtol=0)
        np.testing.assert_allclose(p @ p, p, atol=1e-12, rtol=0)

    def test_koopman_orientation(self):
        k = defect_reference(
            self.successors, [0, 1, 0, 1]
        )["koopman"]
        values = np.array([10.0, 20.0, 30.0, 40.0])
        np.testing.assert_array_equal(
            k @ values, values[self.successors]
        )

    def test_trivial_partitions_also_have_zero_defect(self):
        for labels in ([0, 0, 0, 0], [0, 1, 2, 3]):
            with self.subTest(labels=labels):
                result = defect_reference(self.successors, labels)
                np.testing.assert_allclose(
                    result["defect"], 0.0, atol=1e-12, rtol=0
                )
                self.assertFalse(result["nontrivial_partition"])

    def test_invalid_inputs_are_rejected(self):
        invalid = [
            ([], []),
            ([1, 2], [0, 1]),
            ([0, 1], [0]),
            ([0.0, 1.0], [0, 1]),
        ]
        for successors, labels in invalid:
            with self.subTest(successors=successors, labels=labels):
                with self.assertRaises(ValueError):
                    defect_reference(successors, labels)


if __name__ == "__main__":
    unittest.main(verbosity=2)
