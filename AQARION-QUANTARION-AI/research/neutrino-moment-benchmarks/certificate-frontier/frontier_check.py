from fractions import Fraction as F
from math import comb
from importlib.metadata import version
from flint import fmpq, fmpq_poly

checks = 0

def require(ok, message):
    global checks
    if not ok:
        raise RuntimeError(message)
    checks += 1

def mint(j):
    return F(2, j + 1) if j % 2 == 0 else F(0)

def moment(j):
    return F(1, 10)*mint(j) + (
        5*mint(j + 3) - 3*mint(j + 1)
    )/10

def integrate(poly):
    antiderivative = poly.integral()
    return antiderivative(1) - antiderivative(-1)

def square_coefficients(p):
    out = [F(0)]*(2*len(p))
    for i, a in enumerate(p):
        for j, b in enumerate(p):
            out[i+j] += F(a)*F(b)
            out[i+j+1] -= F(a)*F(b)
    return out

print("AQARION_FLINT_CERTIFICATE_FRONTIER_START")
print("PYTHON_FLINT_VERSION=" + version("python-flint"))
x = fmpq_poly([0, 1])
G = fmpq_poly([
    fmpq(1, 10), fmpq(-3, 10), 0, fmpq(1, 2)
])
catalog = []
for name, p in [
    ("old11", [-8, 24, 20, -51, 84, -100]),
    ("new11", [21, -33, -60, -127, -514, 1000]),
    ("simple13", [0, -1, -1, -3, -6, -25, 50]),
]:
    catalog.append((
        name, (1-x)*fmpq_poly(p)**2, square_coefficients(p)
    ))

for r in range(3, 38):
    catalog.append((
        "power"+str(r), (1-x)**r,
        [F((-1)**j*comb(r, j)) for j in range(r+1)]
    ))

profiles = {
    "equal": lambda j: F(1),
    "linear": lambda j: 1+F(j, 10),
    "geometric": lambda j: F(11, 10)**j,
}
results = []
for name, poly, coefficients in catalog:
    require(
        [F(str(v)) for v in poly.coeffs()] == coefficients,
        name+": coefficient mismatch",
    )
    Z = sum(v*mint(j) for j, v in enumerate(coefficients))
    I = sum(v*moment(j) for j, v in enumerate(coefficients))
    require(Z > 0, name+": nonpositive normalization")
    require(F(str(integrate(poly))) == Z,
            name+": normalization mismatch")
    require(F(str(integrate(poly*G))) == I,
            name+": weighted-integral mismatch")
    normalized = poly/fmpq(Z.numerator, Z.denominator)
    require(F(str(integrate(normalized))) == 1,
            name+": normalized integral mismatch")
    thresholds = {}
    for profile, scale in profiles.items():
        multiplier = sum(
            abs(v)*scale(j) for j, v in enumerate(coefficients)
        )
        require(multiplier > 0, name+": invalid multiplier")
        thresholds[profile] = -I/multiplier
    results.append({
        "name": name, "degree": len(coefficients)-1,
        "thresholds": thresholds,
    })

require(len(results) == 38, "Unexpected catalog size")
expected_equal = {
    "old11": F(35723537, 29654024400),
    "new11": F(515138509, 319709590200),
    "simple13": F(40500847, 19894574700),
    "power37": F(122, 50635),
}
print("SELECTED_CANDIDATE_THRESHOLDS")
for row in results:
    if row["name"] in expected_equal:
        require(
            row["thresholds"]["equal"]
            == expected_equal[row["name"]],
            row["name"]+": reference threshold mismatch",
        )
        for profile, threshold in row["thresholds"].items():
            print(
                row["name"], profile,
                "exact="+str(threshold),
                "display="+format(float(threshold), ".12g"),
            )

print("BEST_IN_THIS_CATALOG")
for budget in (11, 13, 20, 37):
    for profile in profiles:
        eligible = [
            r for r in results
            if r["degree"] <= budget
            and r["thresholds"][profile] > 0
        ]
        require(bool(eligible), "No positive candidate")
        best = max(
            eligible, key=lambda r: r["thresholds"][profile]
        )
        print(
            "budget="+str(budget),
            "profile="+profile,
            "winner="+best["name"],
            "threshold="+format(
                float(best["thresholds"][profile]), ".12g"
            ),
        )

print("FINAL_SUMMARY")
print("CANDIDATES_CHECKED=", len(results))
print("CHECKS_PASSED=", checks)
print("FLINT_FRACTION_COEFFICIENT_AGREEMENT=PASS")
print("FLINT_FRACTION_INTEGRAL_AGREEMENT=PASS")
print("NONNEGATIVITY=BY_EXPLICIT_FACTORED_CONSTRUCTIONS")
print("ERROR_PROFILES=DECLARED_SCENARIOS_NOT_MEASURED_NOISE")
print("THRESHOLDS_REQUIRE_STRICT_INEQUALITY")
print("OPTIMALITY=FINITE_CATALOG_ONLY")
print("FILES_CREATED_BY_PROGRAM=0")
print("INSTALLS_AND_REPOSITORY_ACTIONS=NONE")
print("ALL_CHECKS=PASS")
