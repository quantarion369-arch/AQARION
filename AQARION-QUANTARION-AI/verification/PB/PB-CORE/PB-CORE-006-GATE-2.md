PB-CORE-006 Gate 2 — Semantic gcd-to-lcm Mutation

Purpose

Test whether the Lean development rejects the mathematically incorrect replacement of the gcd-based quantity by an lcm-based quantity.

This is a semantic mutation gate, not a compilation-only gate.

---

Baseline

The intended implementation uses the gcd construction:

listGcd b

For the witness

b = [2, 4]

the intended value is

[
\gcd(2,4)=2.
]

The corresponding witness value is

[
W=5,
\qquad
f_2=9.
]

---

Mutation

Replace

listGcd b

with

b.foldl Nat.lcm 1

For

b = [2,4]

the mutated value is

[
\operatorname{lcm}(2,4)=4.
]

Thus the mutated witness gives

[
W=7,
\qquad
f_2=13.
]

Therefore the mutation changes the mathematical result.

---

Required execution

cd ~/aqarion-lean/AQFPR006

# Baseline
lake build
BASELINE_BUILD_EXIT=$?

# Apply semantic mutation
sed -i 's/listGcd b/b.foldl Nat.lcm 1/' AQFPR006/Basic.lean

lake build
MUTATION_BUILD_EXIT=$?

# Restore
sed -i 's/b.foldl Nat.lcm 1/listGcd b/' AQFPR006/Basic.lean

lake build
RESTORED_BUILD_EXIT=$?

---

Expected disposition

A valid gate requires:

BASELINE_BUILD_EXIT=0
MUTATION_BUILD_EXIT=1
RESTORED_BUILD_EXIT=0

and a semantic witness equivalent to:

MUTATION_WITNESS:
input=[2,4]
expected_gcd_result=9
mutated_lcm_result=13
different=true

---

Interpretation

PASS

All three build conditions hold and the mutation is rejected because it changes the theorem-level result.

FAIL

The mutated implementation compiles and passes the relevant theorem/check despite producing the incorrect lcm semantics.

INCONCLUSIVE

Compilation status is unavailable, the wrong source file was mutated, or the witness does not establish that the mutation actually changes the verified mathematical result.

---

Important

A successful baseline build alone is insufficient.

A successful mutation rejection demonstrates that the formal development is sensitive to the semantic distinction

[
\gcd(2,4)\ne\operatorname{lcm}(2,4).
]

No PASS is asserted by this document until the three runtime exit statuses and the witness are actually observed.
