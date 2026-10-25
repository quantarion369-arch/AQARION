import unittest

class FlintOptionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from flint import fmpz_poly
            cls.poly = fmpz_poly
        except Exception as exc:
            raise unittest.SkipTest(
                f"python-flint unavailable: {type(exc).__name__}: {exc}"
            )

    def test_cyclotomic_divisibility(self):
        fmpz_poly = self.poly
        f = fmpz_poly([1, 0, 0, 1])  # 1 + x^3
        observed = []
        for d in (1, 2, 3, 6):
            phi = fmpz_poly.cyclotomic(d)
            q, r = divmod(f, phi)
            self.assertEqual(q * phi + r, f)
            observed.append(r.is_zero())
        self.assertEqual(observed, [False, True, False, True])

    def test_exact_integer_coefficients(self):
        p = self.poly([1, -2, 0, 4])
        self.assertEqual(list(p.coeffs()), [1, -2, 0, 4])

if __name__ == "__main__":
    unittest.main()
