Burnside M3 Validation — AQ-BURNSIDE-M3-001

Directory: "AQARION-QUANTARION-AI/evidence/BURNSIDE/M3/"

Primary record: "burnside_m3.json"

Recomputation program: "burnside_m3_recompute.py"

Hash manifest: "burnside_m3_hashes.txt"

1. Mathematical statement

Let (C(\lambda)) be the number of set partitions fixed by a permutation with cycle type (\lambda), and let (m_j) be the multiplicity of cycles of length (j) in (\lambda). Define

[
z_\lambda=\prod_{j\geq1} j^{m_j}m_j!.
]

The third Burnside moment is

[
M_3(k)=\frac{1}{k!}\sum_{\sigma\in S_k}C(\sigma)^3
=\sum_{\lambda\vdash k}\frac{C(\lambda)^3}{z_\lambda}.
]

The second equality follows by grouping permutations by cycle type, because the conjugacy class of type (\lambda) has size (k!/z_\lambda). Burnside's lemma also identifies (M_3(k)) as the number of orbits of the diagonal action of (S_k) on ordered triples of set partitions. Thus (M_3(k)) is a nonnegative integer.

2. Current record and discrepancy history

The current JSON record contains values for (1\leq k\leq31), including the corrected entries at (k=25,27,28,29,30). The stored values are not, by themselves, proof of a fresh execution.

The recurrence was reimplemented and run in a separate Python runtime. That run matched all 31 stored values and passed exact-divisibility checks. Separate small-domain controls also passed: direct permutation-level (M_3(k)) for (k\leq5), and direct invariant-partition counts against the recurrence for all 29 cycle types through (k\leq6).

Execution boundary: this was not an execution of the checked-in "burnside_m3_recompute.py" file. A fresh run of that exact file against the repository JSON remains pending.

3. Reproduction command

Run from this directory:

python3 burnside_m3_recompute.py

The program reads "burnside_m3.json" by default, performs direct permutation-level controls for (k\leq5), compares direct invariant-partition counts against the cycle-type recurrence for every cycle type through (k=6), and recomputes the cycle-type third moment for (1\leq k\leq31). Any mismatch exits nonzero.

4. Evidence interpretation

For a repository-bound reproduction receipt, record:

- the repository commit SHA used for the run;
- SHA-256 of "burnside_m3.json", "burnside_m3_recompute.py", and this validation document;
- the exact stdout and process exit code;
- the Python version and execution environment.

The hash manifest binds file bytes; it does not authenticate an execution, prove mathematical correctness by itself, or establish implementation independence. The direct small-domain controls and the cycle-type computation are separate checks, but they are not a fully independent external reproduction.

5. Status boundary

- Stored integer sequence: matched by a separate local recurrence recomputation for (1\leq k\leq31).
- Direct small-domain controls: passed in the local runtime.
- Checked-in repository script freshly executed against current JSON: PENDING.
- Execution receipt bound to repository commit and file hashes: PENDING.
- Formalization: OPEN.
- Promotion: BLOCKED.

Do not promote the evidence until the checked-in script is run against the exact source revision and the execution receipt is recorded and reviewed. A computational pass does not imply Lean/formal verification, independent external reproduction, or proof of any broader claim beyond the stated finite domain.
