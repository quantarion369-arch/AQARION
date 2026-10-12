"""Synthetic function tests; not an end-to-end video validation."""

import unittest
import numpy as np

from causal_estimator import (
    backward_slope,
    analyze_trial,
    features_at_t0,
)


class TestBackwardSlope(unittest.TestCase):

    def test_linear_irregular_sampling(self):
        t = np.array([0.0, 0.03, 0.11, 0.19, 0.31])
        slopes = backward_slope(
            t, 7.0 + 2.5 * t,
            window_s=1.0, min_points=3,
        )
        self.assertTrue(np.isnan(slopes[:2]).all())
        np.testing.assert_allclose(slopes[2:], 2.5, atol=1e-12)

    def test_future_spike_and_centered_negative_control(self):
        t = np.array([0.0, 0.1, 0.2, 0.3, 0.4])
        y = np.array([0.0, 0.1, 0.2, 0.3, 10.0])

        centered = np.gradient(y, t)
        causal = backward_slope(t, y)

        np.testing.assert_allclose(
            centered, [1, 1, 1, 49, 97], atol=1e-10,
        )
        np.testing.assert_allclose(
            causal, [np.nan, np.nan, 1, 1, 49],
            equal_nan=True, atol=1e-10,
        )

        changed = y.copy()
        changed[-1] = 100.0
        other = backward_slope(t, changed)
        np.testing.assert_allclose(
            causal[:-1], other[:-1], equal_nan=True,
        )
        self.assertNotEqual(centered[3], np.gradient(changed, t)[3])

    def test_prefix_consistency(self):
        t = np.linspace(0, 1, 101)
        y = np.sin(3 * t)
        full = backward_slope(t, y)

        for stop in (3, 21, 51, 101):
            prefix = backward_slope(t[:stop], y[:stop])
            np.testing.assert_allclose(
                prefix, full[:stop], equal_nan=True,
            )

    def test_window_boundary(self):
        t = np.array([0.0, 0.1, 0.2, 0.3])
        slopes = backward_slope(t, t, window_s=0.2, min_points=3)
        np.testing.assert_allclose(
            slopes, [np.nan, np.nan, 1, 1], equal_nan=True,
        )

    def test_insufficient_history(self):
        t = np.array([0.0, 0.1, 0.2])
        slopes = backward_slope(t, t, min_points=4)
        self.assertTrue(np.isnan(slopes).all())

    def test_invalid_inputs(self):
        cases = [
            ([0, 0, 1], [1, 2, 3]),
            ([0, 2, 1], [1, 2, 3]),
            ([0, np.nan, 1], [1, 2, 3]),
            ([0, 1, 2], [1, np.inf, 3]),
            ([0, 1, 2], [1, 2]),
        ]
        for t, y in cases:
            with self.subTest(t=t, y=y):
                with self.assertRaises(ValueError):
                    backward_slope(t, y)

        for options in (
            {"window_s": 0},
            {"window_s": np.inf},
            {"min_points": 1},
            {"min_points": 2.5},
            {"min_points": True},
        ):
            with self.subTest(options=options):
                with self.assertRaises(ValueError):
                    backward_slope([0, 1, 2], [0, 1, 2], **options)


class TestGeometryFeatures(unittest.TestCase):

    def setUp(self):
        self.t = np.linspace(0, 1, 101)
        self.xf = 5 + 2 * self.t
        self.xr = 3 * self.t
        self.rf = 1.5 + 0.5 * self.t
        self.rr = 1.5 - 0.3 * self.t

    def analyze(self, **kwargs):
        return analyze_trial(
            self.t, self.xf, self.xr, self.rf, self.rr, **kwargs,
        )

    def test_geometry_and_units(self):
        result = self.analyze()
        np.testing.assert_allclose(result["s"], 5 - self.t)
        np.testing.assert_allclose(
            result["Q"], 0.8 * self.t / (3 + 0.2 * self.t),
        )
        np.testing.assert_allclose(result["dU"][2:], 1, atol=1e-10)

    def test_feature_time_and_future_replacement(self):
        t0 = 0.505
        original = self.analyze()
        chosen = features_at_t0(original, t0)

        self.assertLessEqual(chosen["frame_time_s"], t0)
        self.assertAlmostEqual(chosen["frame_time_s"], 0.5)

        future = self.t > t0
        xf, xr = self.xf.copy(), self.xr.copy()
        rf, rr = self.rf.copy(), self.rr.copy()
        xf[future] = 1000
        xr[future] = -1000
        rf[future] = 100
        rr[future] = 0.01

        changed = analyze_trial(self.t, xf, xr, rf, rr)
        self.assertEqual(chosen, features_at_t0(changed, t0))

        stop = np.searchsorted(self.t, t0, side="right")
        prefix = analyze_trial(
            self.t[:stop], self.xf[:stop], self.xr[:stop],
            self.rf[:stop], self.rr[:stop],
        )
        self.assertEqual(chosen, features_at_t0(prefix, t0))

    def test_missing_history_and_stale_frame(self):
        result = self.analyze()
        with self.assertRaises(ValueError):
            features_at_t0(result, 0.005)
        with self.assertRaises(ValueError):
            features_at_t0(result, -0.1)
        with self.assertRaises(ValueError):
            features_at_t0(result, 1.2, max_frame_age_s=0.02)

    def test_nonpositive_radius(self):
        bad = self.rf.copy()
        bad[5] = 0
        with self.assertRaises(ValueError):
            analyze_trial(self.t, self.xf, self.xr, bad, self.rr)


if __name__ == "__main__":
    unittest.main()
