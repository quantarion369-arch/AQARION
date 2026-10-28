"""Bounded exact analysis. Requests are data, never executable code."""

from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import time
import uuid

from . import recognizer

MAX_STATES = 8
MAX_BODY = 2048

REFERENCE_SHA = (
    "3e7af0579efa8a954e8280dd766df5fc07cc"
    "8b3b38ab73275ead58884d206f17"
)


class ReferenceUnavailable(RuntimeError):
    pass


def decode_request(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON keys are not accepted")
            result[key] = value
        return result

    def nonfinite(_):
        raise ValueError("nonfinite JSON values are not accepted")

    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_constant=nonfinite,
        )
    except (UnicodeError, RecursionError, json.JSONDecodeError) as error:
        raise ValueError("invalid UTF-8 JSON") from error


@lru_cache(maxsize=1)
def _reference():
    # Fixed trusted source; no request can select this path.
    path = (
        Path(__file__).resolve().parents[4]
        / "research" / "separating-register-verification"
        / "cubic-exact-001" / "exact_cubic_check.py"
    )

    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ReferenceUnavailable(
            "preserved exact reference is unavailable"
        ) from error

    if hashlib.sha256(raw).hexdigest() != REFERENCE_SHA:
        raise ReferenceUnavailable(
            "preserved exact reference checksum differs"
        )

    namespace = {
        "__name__": "_trusted_aqarion_exact_reference",
        "__file__": str(path),
    }

    # Only these checksum-pinned local source bytes are loaded.
    exec(compile(raw, str(path), "exec"), namespace)

    return namespace


def analyze(payload):
    started = time.monotonic()

    if not isinstance(payload, dict) or set(payload) != {"T", "h"}:
        raise ValueError("request must contain exactly T and h")

    T = payload["T"]
    h = payload["h"]

    if not isinstance(T, list) or not isinstance(h, list):
        raise ValueError("T and h must be JSON arrays")

    if len(T) not in (2, 4, 8) or len(h) != len(T):
        raise ValueError(
            "use equal-length arrays with two, four, or eight states"
        )

    recognition = recognizer.recognize_extremal(T, h)
    n = len(T)
    d = n.bit_length() - 1

    reference = _reference()
    words = reference["itinerary_words"](T, h)

    profile = []

    for degree in range(d + 1):
        matrix, _ = reference["feature_matrix"](words, n, degree)
        profile.append(reference["exact_rank"](matrix))

    support_size = len(words)

    if recognition["classification"] == "EXTREMAL_REGISTER":
        if profile != recognition["rank_profile_theorem_derived"]:
            raise RuntimeError("normal-form and exact-rank disagreement")

    certificate_checked = None

    if "repair_certificate" in recognition:
        certificate_checked = recognizer.verify_terminal_repair(
            recognition["terminal_truth_table"],
            recognition["repair_certificate"],
        )

        if not certificate_checked or profile[d - 1] != n:
            raise RuntimeError("repair-certificate consistency failure")

    first_full = next(
        (degree for degree, value in enumerate(profile)
         if value == support_size),
        None,
    )

    canonical_input = json.dumps(
        {"T": T, "h": h},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()

    return {
        "mode": "LIVE_BOUNDED_EXACT",
        "analysis_id": uuid.uuid4().hex,
        "computed_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_sha256": hashlib.sha256(canonical_input).hexdigest(),
        "T": T,
        "h": h,
        "state_count": n,
        "distinct_itinerary_count": support_size,
        "observation_separates_states": support_size == n,
        "rank_profile_computed_exactly": profile,
        "minimum_full_degree_on_itinerary_support": first_full,
        "rank_space": (
            "Functions on distinct itineraries; dimension "
            + str(support_size)
        ),
        "recognition": recognition,
        "repair_certificate_checked": certificate_checked,
        "reference_checker_sha256": REFERENCE_SHA,
        "elapsed_ms": round(
            (time.monotonic() - started) * 1000, 3
        ),
        "automatically_saved": False,
        "scope": (
            "Fresh bounded computation, not a saved-case lookup. "
            "No formal verification, novelty determination, "
            "or claim promotion."
        ),
    }
