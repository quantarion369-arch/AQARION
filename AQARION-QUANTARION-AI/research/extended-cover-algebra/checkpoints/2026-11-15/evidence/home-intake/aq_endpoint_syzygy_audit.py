import sympy as s

A,E0,E1,E2,E3,B0,B1,B2,B3,C = x = s.symbols(
    "A E0 E1 E2 E3 B0 B1 B2 B3 C"
)
e = s.symbols("e1:15")
local = {str(v):v for v in (*x,*e)}
weights = (1,1,1,1,1,2,2,2,2,2)

g = [
 E0*B0-A*C,
 E3*B3-E0*B0,
 E3*B3-E1*B1,
 E3*B3-E2*B2,
 -E0*E1*E2+A*B3,
 E0*E1*E3-A*B2,
 -E0*E2*E3+A*B1,
 E1*E2*E3-A*B0,
 -B2*B3+E0*E1*C,
 -B1*B3+E0*E2*C,
 B1*B2-E0*E3*C,
 -B0*B3+E1*E2*C,
 B0*B2-E1*E3*C,
 -B0*B1+E2*E3*C
]

text = """
-A*e4+E3*e5+E2*e6
A*e3-E3*e5+E1*e7
-A*e2+E3*e5+E0*e8
-E2*E3*e2+E2*E3*e3+B0*e7+B1*e8
E2*E3*e1+B0*e7+A*e14
-E1*E3*e2+E1*E3*e4-B0*e6+B2*e8
-E1*E3*e1+B0*e6+A*e13
-E1*E2*e2+B0*e5+B3*e8
E1*E2*e1+B0*e5+A*e12
B0*e1+B0*e2-C*e8+E3*e12
-B0*e1-B0*e2+B0*e4+C*e8+E2*e13
B0*e1+B0*e2-B0*e3-C*e8+E1*e14
E0*E3*e3-E0*E3*e4+B1*e6+B2*e7
-E0*E3*e1-E0*E3*e2+E0*E3*e3+B1*e6+A*e11
E0*E2*e3-B1*e5+B3*e7
E0*E2*e1+E0*E2*e2-E0*E2*e3+B1*e5+A*e10
B1*e1+B1*e2+C*e7+E3*e10
-B1*e1-B1*e2+B1*e4-C*e7+E2*e11
B1*e1+C*e7+E0*e14
-E0*E1*e4+B2*e5+B3*e6
E0*E1*e1+E0*E1*e2-E0*E1*e4+B2*e5+A*e9
B2*e1+B2*e2-C*e6+E3*e9
-B2*e1-B2*e2+B2*e3+C*e6+E1*e11
-B2*e1+C*e6+E0*e13
B3*e1+B3*e2-B3*e4+C*e5+E2*e9
B3*e1+B3*e2-B3*e3+C*e5+E1*e10
B3*e1+C*e5+E0*e12
C*E3*e2-C*E3*e3-B0*e11+B1*e13
-C*E3*e2+C*E3*e4+B0*e11+B2*e14
-C*E2*e2+C*E2*e3-B0*e10+B1*e12
-C*E2*e2-B0*e10+B3*e14
-C*E1*e2+C*E1*e4-B0*e9+B2*e12
C*E1*e2+B0*e9+B3*e13
-C*E0*e3+C*E0*e4-B1*e9+B2*e10
C*E0*e3+B1*e9+B3*e11
"""

expressions = [
    s.expand(s.sympify(line, locals=local))
    for line in text.strip().splitlines()
]
assert len(expressions) == 35

D2 = s.Matrix.hstack(*[
    s.Matrix([q.coeff(v) for v in e])
    for q in expressions
])

for j,q in enumerate(expressions):
    assert s.expand(q-sum(D2[i,j]*e[i] for i in range(14))) == 0

row_shifts = [3]*8+[4]*6
column_shifts = [4]*3+[5]*24+[6]*8
zero = dict.fromkeys(x,0)

print("RECONSTRUCTED ENDPOINT SYZYGY AUDIT", flush=True)
print("Ring: QQ[A,E0,E1,E2,E3,B0,B1,B2,B3,C]")
print("Weights:", weights)
print("Matrix shape:", D2.shape)
print("Column shifts: 4^3, 5^24, 6^8")

failed = False
for j in range(35):
    residual = s.expand(sum(g[i]*D2[i,j] for i in range(14)))
    homogeneous = True
    constants_zero = True
    for i in range(14):
        coefficient = D2[i,j]
        if coefficient == 0:
            continue
        required = column_shifts[j]-row_shifts[i]
        degrees = {
            sum(a*b for a,b in zip(m,weights))
            for m,c in s.Poly(coefficient,*x,domain=s.QQ).terms()
            if c
        }
        homogeneous &= degrees == {required}
        constants_zero &= coefficient.subs(zero) == 0

    ok = residual == 0 and homogeneous and constants_zero
    failed |= not ok
    print(
        f"Q{j+1:02d}: relation={'PASS' if residual == 0 else 'FAIL'} "
        f"degree={'PASS' if homogeneous else 'FAIL'} "
        f"zero-constants={'PASS' if constants_zero else 'FAIL'}",
        flush=True
    )

print("\nRESULT:", "FAIL" if failed else "35/35 PASS")
print("This verifies delta1 * reconstructed_D2 = 0 exactly over QQ.")
print("It also verifies the claimed shifts and zero constant terms.")
print("It does NOT identify Q1,...,Q35 with the saved S1,...,S35.")
print("It does NOT independently prove global kernel generation.")
print("No research files were modified.")
raise SystemExit(1 if failed else 0)
