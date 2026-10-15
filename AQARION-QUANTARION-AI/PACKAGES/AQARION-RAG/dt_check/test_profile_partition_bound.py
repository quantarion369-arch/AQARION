import itertools, os, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import closure_profile as cp

def rgs(n):
    def rec(i, lab, m):
        if i == n: yield tuple(lab); return
        for l in range(m + 1):
            lab.append(l); yield from rec(i + 1, lab, max(m, l + 1) if l == m else m); lab.pop()
    yield from rec(0, [], 0)

def stable_size(T, lab):
    cur = list(lab); cnt = len(set(cur))
    while True:
        mp = {}
        new = [mp.setdefault((cur[x], cur[T[x]]), len(mp)) for x in range(len(T))]
        if len(mp) == cnt: return cnt
        cur, cnt = new, len(mp)

def delta_of(T, lab):
    n, k = len(T), max(lab) + 1
    basis = [[1 if lab[x] == b else 0 for x in range(n)] for b in range(k)]
    prof = list(cp.closure_profile(list(T), basis)["profile"])
    assert prof and prof[-1] == 0
    return k, tuple(prof[:-1])

def bound(k, delta):
    prod = 1
    for d in delta: prod *= 1 + d
    return k * (prod - 1)

class ProfileBound(unittest.TestCase):
    def _sweep(self, n):
        checked = 0
        for T in itertools.product(range(n), repeat=n):
            for lab in rgs(n):
                k, delta = delta_of(T, lab); s = stable_size(T, lab)
                with self.subTest(n=n, T=T, lab=lab):
                    self.assertLessEqual(sum(delta), s - k)
                    self.assertLessEqual(s - k, bound(k, delta))
                checked += 1
        return checked

    def test_exhaustive_n_le_4(self):
        self.assertEqual(sum(self._sweep(n) for n in range(1, 5)), 3984)

    @unittest.skipUnless(os.environ.get("AQ_DEEP") == "1", "set AQ_DEEP=1 for n=5")
    def test_exhaustive_n5(self):
        self.assertEqual(self._sweep(5), 162500)

    def test_upper_bound_is_attained(self):
        T, lab = (0, 0, 1, 1), (0, 1, 0, 1)
        k, delta = delta_of(T, lab)
        self.assertEqual((k, delta), (2, (1,)))
        self.assertEqual(stable_size(T, lab) - k, bound(k, delta))

    def test_negative_control_off_by_one_bound_is_rejected(self):
        T, lab = (0, 0, 1, 1), (0, 1, 0, 1)
        k, delta = delta_of(T, lab)
        self.assertGreater(stable_size(T, lab) - k, bound(k, delta) - 1)

    def test_oracle_on_hand_cases(self):
        self.assertEqual(stable_size((0, 1), (0, 1)), 2)
        self.assertEqual(stable_size((1, 1), (0, 0)), 1)
        self.assertEqual(stable_size((0, 0, 1, 1), (0, 1, 0, 1)), 4)

if __name__ == "__main__":
    unittest.main()
