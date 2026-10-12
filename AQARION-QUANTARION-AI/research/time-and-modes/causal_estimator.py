"""Past-only geometry features. No video tracking is implemented here."""

import numpy as np


def _validate_pair(t, values):
    t = np.asarray(t, dtype=float)
    values = np.asarray(values, dtype=float)

    if t.ndim != 1 or values.shape != t.shape:
        raise ValueError("Expected matching 1-D arrays")
    if len(t) < 2:
        raise ValueError("At least two samples are required")
    if not np.all(np.isfinite(t)):
        raise ValueError("Times must be finite")
    if not np.all(np.isfinite(values)):
        raise ValueError("Values must be finite")
    if np.any(np.diff(t) <= 0):
        raise ValueError("Times must be strictly increasing")
    return t, values


def backward_slope(t, values, window_s=0.20, min_points=3):
    """Trailing least-squares slope; units are value units per second."""
    t, values = _validate_pair(t, values)

    if not np.isfinite(window_s) or window_s <= 0:
        raise ValueError("window_s must be finite and positive")
    if (
        not isinstance(min_points, (int, np.integer))
        or isinstance(min_points, (bool, np.bool_))
        or min_points < 2
    ):
        raise ValueError("min_points must be an integer >= 2")

    slopes = np.full(len(t), np.nan)

    for i in range(len(t)):
        tolerance = (
            8 * np.finfo(float).eps
            * max(1.0, abs(t[i]), window_s)
        )
        cutoff = t[i] - window_s - tolerance
        start = np.searchsorted(t, cutoff, side="left")

        ts = t[start:i + 1]
        ys = values[start:i + 1]

        if len(ts) < min_points:
            continue

        dt = ts - ts.mean()
        denominator = np.dot(dt, dt)
        if denominator <= 0:
            raise ValueError("Numerically unresolved time differences")

        slopes[i] = np.dot(dt, ys - ys.mean()) / denominator

    return slopes


def analyze_trial(
    t, x_front, x_rear, R_front, R_rear,
    window_s=0.20, min_points=3,
):
    """
    Positions/radii are in cm; time is in seconds.
    'front' and 'rear' remain fixed identities from emission order.
    """
    t, xf = _validate_pair(t, x_front)
    _, xr = _validate_pair(t, x_rear)
    _, rf = _validate_pair(t, R_front)
    _, rr = _validate_pair(t, R_rear)

    if np.any(rf <= 0) or np.any(rr <= 0):
        raise ValueError("Ring radii must be positive")

    Q = (rf - rr) / (rf + rr)
    uf = backward_slope(t, xf, window_s, min_points)
    ur = backward_slope(t, xr, window_s, min_points)

    return {
        "t": t.copy(),
        "s": xf - xr,
        "Q": Q,
        "U_front": uf,
        "U_rear": ur,
        "dU": ur - uf,
        "dQ": backward_slope(t, Q, window_s, min_points),
    }


def features_at_t0(result, t0, max_frame_age_s=None):
    """Select available features; never interpolate from later frames."""
    if not np.isfinite(t0):
        raise ValueError("t0 must be finite")

    if max_frame_age_s is not None:
        if (
            not np.isfinite(max_frame_age_s)
            or max_frame_age_s < 0
        ):
            raise ValueError("max_frame_age_s must be finite and >= 0")

    times = np.asarray(result["t"], dtype=float)
    i = np.searchsorted(times, t0, side="right") - 1
    if i < 0:
        raise ValueError("No frame at or before t0")

    frame_time = float(times[i])
    age = float(t0 - frame_time)

    if max_frame_age_s is not None and age > max_frame_age_s:
        raise ValueError("Selected frame is too old")

    features = {
        name: float(result[name][i])
        for name in ("s", "dU", "Q", "dQ")
    }
    if not all(np.isfinite(v) for v in features.values()):
        raise ValueError("Insufficient past samples for slope estimation")

    return {
        "requested_t0_s": float(t0),
        "frame_time_s": frame_time,
        "frame_age_s": age,
        "features": features,
      }
