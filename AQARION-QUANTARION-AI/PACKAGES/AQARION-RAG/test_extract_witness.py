import itertools
#!/usr/bin/env python3
import unittest
from extract_witness import extract_diagnostic
from wire_corpus_assessment import to_assess_witness
from assess import READINGS, make_claim, assess

class ExtractDiagnosticTests(unittest.TestCase):
    def test_extracts_candidate(self):
        candidate, reason = extract_diagnostic("quadratic c = 0.5 unstable")
        self.assertIsNone(reason)
        self.assertEqual(candidate["c"], 0.5)
        self.assertEqual(candidate["reported_label"], "unstable")
        self.assertEqual(candidate["verification_status"], "SYNTACTIC_CANDIDATE_ONLY")

    def test_rejects_missing_family(self):
        candidate, reason = extract_diagnostic("c = 0.5 unstable")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "missing_family_marker")

    def test_rejects_missing_parameter(self):
        candidate, reason = extract_diagnostic("quadratic unstable")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "missing_parameter_c")

    def test_rejects_missing_label(self):
        candidate, reason = extract_diagnostic("quadratic c = 0.5")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "missing_stability_label")

    def test_rejects_conflicting_labels(self):
        candidate, reason = extract_diagnostic("quadratic c = 0.5 stable but unstable")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "conflicting_stability_labels")

class AssessmentTests(unittest.TestCase):
    def claim(self):
        return make_claim("universal bounded-orbit stability", lambda w: True, READINGS["bounded_orbit"])

    def test_lying_label_does_not_change_verdict(self):
        witness = to_assess_witness({
            "id": "T1", "family": "quadratic", "c": 0.5,
            "reported_label": "stable",
        })
        verdict, decisive = assess(self.claim(), [witness])
        self.assertEqual(verdict, "REFUTED")
        self.assertEqual(decisive, ["T1"])

    def test_stable_parameter_is_not_decisive(self):
        witness = to_assess_witness({
            "id": "T2", "family": "quadratic", "c": 0.2,
            "reported_label": "unstable",
        })
        verdict, decisive = assess(self.claim(), [witness])
        self.assertEqual(verdict, "OPEN")
        self.assertEqual(decisive, [])

    def test_corpus_candidate_refutes_universal_claim(self):
        witness = to_assess_witness({
            "id": "T3", "family": "quadratic", "c": 1.5,
            "reported_label": "unstable",
        })
        verdict, decisive = assess(self.claim(), [witness])
        self.assertEqual(verdict, "REFUTED")
        self.assertEqual(decisive, ["T3"])

if __name__ == "__main__":
    unittest.main()

class DualReadingTests(unittest.TestCase):
    def test_both_readings_refute_c_half(self):
        from assess import READINGS, make_claim, assess
        from wire_corpus_assessment import to_assess_witness
        witness = to_assess_witness({
            "id": "D1",
            "family": "quadratic",
            "c": 0.5,
            "reported_label": "stable",
        })
        for reading in READINGS:
            claim = make_claim(
                "universal " + reading + " stability",
                lambda w: True,
                READINGS[reading],
            )
            verdict, decisive = assess(claim, [witness])
            self.assertEqual(verdict, "REFUTED")
            self.assertEqual(decisive, ["D1"])

class ScopedClaimTests(unittest.TestCase):
    def witnesses(self):
        from wire_corpus_assessment import to_assess_witness
        return [
            to_assess_witness({
                "id": "S1", "family": "quadratic", "c": -2.0,
                "reported_label": "stable",
            }),
            to_assess_witness({
                "id": "S2", "family": "quadratic", "c": 0.2,
                "reported_label": "unstable",
            }),
        ]

    def claim(self):
        from assess import READINGS
        return make_claim(
            "bounded-orbit stability for -2 <= c <= 0.25",
            lambda w: -2 <= w["c"] <= 0.25,
            READINGS["bounded_orbit"],
        )

    def attracting_claim(self):
        from assess import READINGS
        return make_claim(
            "attracting-fixed-point stability for -2 <= c <= 0.25",
            lambda w: -2 <= w["c"] <= 0.25,
            READINGS["attracting_fixed_point"],
        )

    def test_bounded_orbit_scoped_claim_is_open(self):
        verdict, decisive = assess(self.claim(), self.witnesses())
        self.assertEqual(verdict, "OPEN")
        self.assertEqual(decisive, [])

    def test_attracting_reading_refutes_scoped_claim(self):
        verdict, decisive = assess(self.attracting_claim(), self.witnesses())
        self.assertEqual(verdict, "REFUTED")
        self.assertEqual(decisive, ["S1"])

class GeneratorDeterminismTests(unittest.TestCase):
    def test_generator_reproduces_committed_document(self):
        import subprocess
        from pathlib import Path
        committed = subprocess.run(
            ["git", "show", "HEAD:./corpus/quadratic-stability-witnesses.md"],
            capture_output=True, text=True, check=True,
        ).stdout
        regenerated = subprocess.run(
            ["python", "make_quadratic_stability_evidence.py"],
            capture_output=True, text=True, check=True,
        )
        current = Path("corpus/quadratic-stability-witnesses.md").read_text()
        self.assertEqual(regenerated.stdout.count("The quadratic map with c ="), 10)
        self.assertEqual(current, committed)

class IsomorphismBijectionTests(unittest.TestCase):
    """Fix(T*) ~= Con(T|_P): full bijection, not just cardinality match."""
    def _partitions(self, n):
        def helper(rem, cur):
            if not rem:
                yield [b[:] for b in cur]; return
            x, rest = rem[0], rem[1:]
            for i, b in enumerate(cur):
                nxt = [bb[:] for bb in cur]; nxt[i].append(x)
                yield from helper(rest, nxt)
            yield from helper(rest, cur + [[x]])
        yield from helper(list(range(1, n)), [[0]])

    def _fix(self, T, n):
        out = []
        for P in self._partitions(n):
            b = {x: i for i, bl in enumerate(P) for x in bl}
            if any(len({b[T[x]] for x in bl}) > 1 for bl in P): continue
            if any(b[T[x]] == b[T[y]] and b[x] != b[y]
                   for x in range(n) for y in range(n)): continue
            out.append(P)
        return out

    def _core(self, T, n):
        X = set(range(n))
        for _ in range(n): X = {T[x] for x in X}
        return sorted(X)

    def _con(self, T, P):
        out = []
        for parts in self._partitions(len(P)):
            orig = [[P[i] for i in bl] for bl in parts]
            b = {x: i for i, bl in enumerate(orig) for x in bl}
            if any(len({b[T[p]] for p in bl}) > 1 for bl in orig): continue
            if any(b[T[x]] == b[T[y]] and b[x] != b[y] for x in P for y in P): continue
            out.append(orig)
        return out

    def _canon(self, blocks):
        return str(sorted(sorted(b) for b in blocks))

    def _phi(self, E, P):
        b = {x: i for i, bl in enumerate(E) for x in bl}
        comps = {}
        for p in P: comps.setdefault(b[p], []).append(p)
        return sorted(sorted(v) for v in comps.values())

    def _psi(self, F, T, n, P):
        def Tn(x):
            for _ in range(n): x = T[x]
            return x
        bF = {x: i for i, bl in enumerate(F) for x in bl}
        sig = {x: bF[Tn(x)] for x in range(n)}
        comps = {}
        for x in range(n): comps.setdefault(sig[x], []).append(x)
        return sorted(sorted(v) for v in comps.values())

    def test_phi_psi_bijection_n2_to_5(self):
        for n in range(2, 6):
            for T in itertools.product(range(n), repeat=n):
                T = list(T)
                P = self._core(T, n)
                if not all(T[p] in P for p in P): continue
                fix = self._fix(T, n)
                con = self._con(T, P)
                images = [self._canon(self._phi(E, P)) for E in fix]
                self.assertEqual(len(set(images)), len(fix), f"phi not injective n={n} T={T}")
                self.assertEqual(set(images), {self._canon(c) for c in con},
                                 f"phi not surjective n={n} T={T}")
                for E in fix:
                    self.assertEqual(self._canon(self._psi(self._phi(E, P), T, n, P)),
                                     self._canon(E), f"roundtrip fail n={n} T={T}")
