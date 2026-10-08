Burnside M3 Validation — AQ-BURNSIDE-M3-001

Directory: "AQARION-QUANTARION-AI/evidence/BURNSIDE/M3/"

Primary record: "burnside_m3.json"

Recomputation program: "burnside_m3_recompute.py"

Hash manifest: "burnside_m3_hashes.txt"

1. Mathematical statement

Let (C(\lambda)) be the number of set partitions fixed by a permutation with cycle type (\lambda), and let (m_j) be the multiplicity of cycles of length (j) in (\lambda). Define

[
z_\lambda=\prod_{j\geq1}j^{m_j}m_j!.
]

The third Burnside moment is

[
M_3(k)=\frac{1}{k!}\sum_{\sigma\in S_k}C(\sigma)^3
=\sum_{\lambda\vdash k}\frac{C(\lambda)^3}{z_\lambda}.
]

The second equality follows by grouping permutations by cycle type, because the conjugacy class of type (\lambda) has size (k!/z_\lambda). Burnside's lemma also identifies (M_3(k)) as the number of orbits of the diagonal action of (S_k) on ordered triples of set partitions. Thus (M_3(k)) must be a nonnegative integer.

2. Current record and known discrepancy history

The current JSON record contains the corrected integers for (1\leq k\leq31), including the previously disputed entries at (k=25,27,28,29,30). The correction history is not itself proof of a fresh execution: the stored values must be compared with a run of the checked-in program against the checked-in JSON.

A previous validation document had been concatenated with an older specification containing ellipses and malformed formula placeholders. This replacement removes that conflicting appended text.

3. Reproduction command

Run from this directory:

python3 burnside_m3_recompute.py

The program reads "burnside_m3.json" by default, performs direct permutation-level controls for (k\leq5), compares direct invariant-partition counts against the cycle-type recurrence for every cycle type through (k=6), and recomputes the cycle-type third moment for (1\leq k\leq31). Any mismatch exits nonzero.

4. Evidence interpretation

The script's success messages are outputs of the validation program; they are not proof that a run occurred merely because they appear in a file or prior conversation. A current run should be captured together with:

- The repository commit SHA used for the run.
- SHA-256 of "burnside_m3.json", "burnside_m3_recompute.py", and this validation document.
- The exact stdout and exit code.
- The Python version and execution environment.

The hash manifest binds file bytes; it does not authenticate a run, prove mathematical correctness by itself, or establish implementation independence. The direct small-domain controls and the cycle-type computation are separate checks, but they share the same program and are not a fully independent external reproduction.

5. Status boundary

- Stored integer sequence: corrected values are present in the current JSON record.
- Fresh execution authenticated to current source revision: PENDING.
- Formalization: OPEN.
- Promotion: BLOCKED.

Do not promote the evidence until a fresh run is recorded against the exact source revision and its outputs are reviewed. A computational pass does not imply Lean/formal verification, independent external reproduction, or proof of any broader claim beyond the stated finite domain.
