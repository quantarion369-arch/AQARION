PB-CORE — Replay and Governance Instructions

Date: 2026-10-09
Purpose: Reproducible replay of the PB-CORE-004 bounded audit and PB-CORE-006 arithmetic verifier.

1. File inventory

All paths are relative to the repository root.

File| Purpose
"AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-004-PERIODIC-CORE-PROOF.md"| Paper theorem and proof
"AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-004-DIRECT-PULLBACK-AUDIT-2026-10-06-BOUND-v2.py"| Bounded direct oracle and core-extension comparison
"AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-004-DIRECT-PULLBACK-AUDIT-RECEIPT.json"| Audit provenance and status
"AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-006-THEOREM.md"| Aggregate-count candidate and proof obligations
"AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-006-ARITHMETIC-VERIFY.py"| Exact formula arithmetic
"AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-006_RECEIPT.json"| Formula status and provenance
"AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-REPLAY-AND-GOVERNANCE.md"| This replay and governance record

2. Environment

The Python scripts use only the standard library. Record the Python version, operating system, architecture, Git commit, and execution output in the audit log.

From the repository root:

python3 --version
git rev-parse HEAD
git status --short

3. Replay PB-CORE-004

python3 AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-004-DIRECT-PULLBACK-AUDIT-2026-10-06-BOUND-v2.py 6 AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-004-DIRECT-PULLBACK-AUDIT-RECEIPT.json

Expected acceptance conditions for a successful fresh run:

- The script exits with status 0.
- The total map count is 50,069 for (n=1,\ldots,6).
- Every tested map has zero candidate/oracle mismatches.
- The constant-map and identity-map controls on two points return 1 and 2 fixed partitions, respectively.
- The universal-only mutation is rejected.
- The receipt records the actual source hash and execution environment.

The receipt's historical numbers are not a substitute for this replay.

4. Replay PB-CORE-006 arithmetic

python3 AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-006-ARITHMETIC-VERIFY.py 12

Expected acceptance conditions:

- The script exits with status 0.
- Every computed formula value matches the corresponding supplied reference value.
- Every factorial ratio is evaluated with exact integer arithmetic.
- No floating-point arithmetic is used.

A successful arithmetic run verifies evaluation of the displayed expression. It does not prove the expression counts the intended mathematical objects.

5. Hash the exact saved files

sha256sum \
  AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-004-PERIODIC-CORE-PROOF.md \
  AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-004-DIRECT-PULLBACK-AUDIT-2026-10-06-BOUND-v2.py \
  AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-006-THEOREM.md \
  AQARION-QUANTARION-AI/verification/PB/PB-CORE/PB-CORE-006-ARITHMETIC-VERIFY.py

Record these newly computed hashes in the replay log. Do not reuse a historical hash unless the bytes match exactly.

6. Evidence labels

- PAPER_PROOF: a mathematical argument has been written; it is not thereby Lean-certified.
- ARITHMETIC_REPLAYED: the exact formula implementation ran and matched its supplied reference values.
- BOUNDED_AUDIT_REPLAYED: the independent candidate and direct oracle completed the declared finite census with zero mismatches.
- PROVENANCE_AUTHENTICATED: source and receipt bytes have been tied to a specific repository commit and hash.
- LEAN_VERIFIED: the formalization builds successfully with no unresolved proof obligations under the project's declared policy.

These labels are independent. Passing one does not imply passing another.

7. Promotion gate

Do not promote PB-CORE-006 to a theorem based only on arithmetic agreement or finite enumeration. Promotion requires a reviewed general derivation and the project's required formal verification.

Until those requirements are met:

- Lean: OPEN.
- C4: BLOCKED.
- Publication: BLOCKED.
- Promotion: FALSE.
