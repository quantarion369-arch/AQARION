### AQARION — repository audit, 8 October 2026

I inspected the live public repository through GitHub, including the default branch, its recursive file tree, the periodic-core proof, the JOIN-STABILITY verifier, the claim registry, and the Burnside evidence records.

Repository: [quantarion369-arch/AQARION](https://github.com/quantarion369-arch/AQARION)

### Highest-priority finding

JOIN-STABILITY has a reproducibility blocker in the live tree.

`AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/verify.py` requires `manifest.json`, and `reproduce.sh` also explicitly checks for it. The recursive tree does not contain that file, and the GitHub contents endpoint returns `404` for that exact path.

Consequence: the documented reproduction entrypoint will stop before running the verifier. This is a repository defect, not a mathematical counterexample.

The live `main` tree SHA inspected was:

`f0b50e20b7c1e4f1219a4d96714bfea899bf7f8e`

I have not changed the repository.

Worked for 48s

### 1\. Exact repository actions required

A. Restore a valid JOIN-STABILITY manifest

Required path

`AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/manifest.json`

The repository's own README declares this manifest authoritative. My GitHub history query returned no commits for this exact path, so I cannot recover an earlier version from that history query. Do not fabricate a replacement schema; define the schema against the existing package contract.

Affected files

`AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/README.md` `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/reproduce.sh` `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/verify.py`

B. Correct the evidence-class mismatch

Exact file

`AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/evidence.jsonl`

Record `EV-JS-002` labels `verify.py` as `[V]` computational verification. But the live verifier explicitly says mathematical verification has not yet been added; it checks package structure and claim/evidence references.

Required correction: either implement the declared mathematical check and test it, or downgrade that evidence record to accurately describe the current implementation. Do not label a structural package check as mathematical verification.

### 2\. What the existing verifier actually establishes

File: `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/verify.py`

Its current successful path checks:

* Required files and directories exist.

* JSON and JSONL records parse.

* Claim and evidence IDs are unique.

* Evidence records reference existing claims.

It does not independently establish the JOIN-STABILITY theorem. The source code says so explicitly. This is a good separation of concerns in principle, but the evidence record must match the implementation.

I have not run the repository's code in a local execution environment during this audit. The reproduction failure above follows from the live file tree and the explicit manifest check in `reproduce.sh`; it is not a claimed test execution.

### 3\. CI status — scoped correctly

The latest workflow returned by the repository's Actions API was AQARION Mobile Research Kit Validation, run on 8 October 2026, with conclusion `success`. [View the workflow run](https://github.com/quantarion369-arch/AQARION/actions/runs/37709152608).

That is evidence for the Mobile Research Kit workflow only. It does not establish that JOIN-STABILITY reproduces successfully.

### 4\. Literature boundary

Two relevant sources reinforce the need to keep the mathematical claim narrow:

* Jakubíková-Studenovská and Janičková, [Congruence lattices of connected monounary algebras](https://doi.org/10.1007/s00012-020-00686-2), Algebra Universalis 81, article 54 (2020). This establishes relevant prior work on congruence lattices of unary algebras.

* Syrovatskaya, [Monounary algebras with periodic endomorphism semigroups](https://doi.org/10.4213/dm1886), Diskretnaya Matematika 38(1) (2026), 121–134. This is a recent related source on finite unary algebras and periodic endomorphism semigroups.

These sources do not, by themselves, settle the novelty of AQARION's particular theorem or its evidence pipeline. That comparison remains open.

### 5\. Current disposition

| Item                               | Audit result                                          |
| ---------------------------------- | ----------------------------------------------------- |
| Live repository and default branch | Inspected                                             |
| JOIN-STABILITY manifest            | Missing                                               |
| JOIN-STABILITY reproduction        | Blocked by missing manifest                           |
| Mathematical verification label    | Needs correction or implementation                    |
| Mobile Research Kit CI             | Success; different workflow                           |
| PB-CORE-004 paper proof            | Present in repository; Lean remains open per artifact |
| Literature novelty                 | Open                                                  |
| Repository modifications by me     | None                                                  |

The one task I recommend you perform first: fix the JOIN-STABILITY manifest/verifier contract. Then rerun `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/reproduce.sh` and preserve its actual output. Do not promote the claim based on that run unless the mathematical verification and its evidence record genuinely support the promotion.

No new identifiers, folders, or architectural layers are needed for this repair.
Worked for 48s

### Repair artifact: manifest contract

The README and ZIP-clone specification provide enough information to define a minimal proposed schema, but not enough to claim that a historical manifest has been recovered. The following is a schema proposal, not a verified replacement file.

# JOIN-STABILITY manifest contract

The canonical manifest must identify the package and its provenance. It must not store a mathematical PASS that the verifier merely repeats.

Required fields:

- `schema_version`: manifest schema version.
- `package_id`: stable package identity, `JOIN-STABILITY`.
- `package_version`: package release identifier.
- `source_revision`: full Git commit SHA from which the package was assembled.
- `claims`: declared claim identifiers, consistent with `claims.jsonl`.
- `dependencies`: explicitly declared runtime or verification dependencies.

Validation requirements:

- The top-level value must be a JSON object.
- All required fields must be present and correctly typed.
- `package_id` must equal `JOIN-STABILITY`.
- `source_revision` must be a full commit identifier, not a branch name.
- Claim references must agree with the claim registry.
- The manifest must not certify a theorem merely because its JSON parses.
- Missing required files must cause a nonzero verifier exit.
- The manifest must not be silently regenerated during reproduction.

Before adopting this contract, compare it with any surviving package archives or historical release artifacts. Do not treat this proposed schema as a recovered original.

### Evidence-class correction

The live `evidence.jsonl` contains this record:

```json
{"evidence_id":"EV-JS-002","claim_id":"JS-11","class":"[V]","type":"computational-verification","artifact":"verify.py","status":"IMPLEMENTATION_TARGET","description":"Independent executable verification of declared finite fixtures."}
```

The class and description overstate what the current implementation performs. Here is a conservative replacement that preserves the existing evidence identifier and makes the scope explicit:

{"evidence_id":"EV-JS-002","claim_id":"JS-11","class":"[R]","type":"structural-package-validation","artifact":"verify.py","status":"IMPLEMENTED_STRUCTURAL_ONLY","description":"Checks required package structure, JSON/JSONL parsing, identifier uniqueness, and claim/evidence references. Does not independently verify the JOIN-STABILITY theorem or compute the declared finite fixtures."}

This correction makes the record more honest, but it does not by itself solve the claim-association problem: the evidence remains linked to `JS-11`, the theorem target. The registry and its evidence references must be reviewed together so that structural validation cannot be mistaken for evidence supporting the theorem.

### Mathematical work: the theorem needs a separate proof check

The target is

T^{-1}(E)\\le E,\\quad T^{-1}(F)\\le F
\\quad\\Longrightarrow\\quad
T^{-1}(E\\vee F)\\le E\\vee F

for finite .

A useful preliminary lemma is the finite quotient argument. For an equivalence relation , let be the quotient map and . The assumption says

g(x)=g(y)\\implies q(x)=q(y).

Thus the kernel partition of refines the kernel partition of . Since has at most distinct values, the refinement cannot have more classes than ; it follows that the two kernel partitions agree. Hence

\\boxed{xEy\\iff T(x)E T(y).}

The same conclusion holds for .

Adversarial proof obligation: these two equivalences alone are not a substitute for a checked join argument. The critical step is proving that the join relation also reflects relatedness through . The repository's own architecture identifies this as the join-chain and chain-lifting work. That step should be proved explicitly, not inferred from the individual quotient results.

The verifier must not claim to check this lemma or the join theorem until an independent implementation and appropriate finite fixtures have actually been added.

### Reproduction commands for the maintainer

After restoring the missing files and reconciling their schemas, run these commands from the package directory:

```sh
cd AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY

python3 -m json.tool manifest.json >/dev/null
python3 verify.py
./reproduce.sh
printf 'REPRODUCE_EXIT=%s\n' "$?"
```

The commands above are proposed acceptance steps; they have not been executed in this audit. A zero exit from the current structural verifier would establish only that its declared checks completed, not that the theorem was proved.

For the repaired package, preserve the raw output and exit code, record the full source commit SHA, and verify that the manifest's `source_revision` matches that snapshot. Run the mathematical fixture verifier separately once it exists, with positive and negative controls.

### Literature boundary

The nearby literature reinforces the need to distinguish a finite unary-algebra theorem from the tooling used to check its implementation.

* Syrovatskaya, Monounary algebras with periodic endomorphism semigroups (2026), studies endomorphism-semigroup properties of unary algebras and characterizes periodicity in this setting. It is relevant background, but it does not by itself establish or refute the particular JOIN-STABILITY theorem.

* Jakubíková-Studenovská, Pöschel, and Radeleczki, The minimal closed monoids for the Galois connection End–Con (2024), concerns endomorphism monoids and congruence lattices of finite algebras. It is useful context for positioning work on congruences, not evidence of novelty for this specific theorem.

The novelty question remains open. The immediate goal is correctness and reproducibility, not a novelty claim.

### Final audit disposition

| Item                         | Disposition                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------ |
| manifest.json                | Missing in connected live-file lookup; restore against the documented contract |
| claims.jsonl                 | Also returned 404; verify at the same exact commit                             |
| EV-JS-002                    | Downgrade to structural evidence or implement genuine mathematical checking    |
| Join theorem                 | Mathematical proof obligation remains distinct from package verification       |
| Reproduction run             | Not executed here                                                              |
| Repository mutations         | None                                                                           |
| C4 / publication / promotion | Unchanged: BLOCKED / BLOCKED / FALSE                                           |

Next action: establish the exact commit's complete JOIN-STABILITY tree, recover or define the manifest against surviving package artifacts, and reconcile the claim registry before running reproduction. That avoids repairing one missing file only to discover that the package remains internally incomplete.
Worked for 30s

### `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/manifest.json`

Deliverable — manifest template

```json

{
  "schema_version": "1.0",
  "package_id": "JOIN-STABILITY",
  "package_version": "0.1.0",
  "status": "BLOCKED_PENDING_REPRODUCTION",
  "source_revision": "REPLACE_WITH_FULL_GIT_COMMIT_SHA",
  "verification_policy": {
    "fail_closed": true,
    "allow_automatic_manifest_generation": false,
    "mathematical_verification_status": "NOT_ESTABLISHED_BY_STRUCTURAL_VALIDATION"
  },
  "required_artifacts": [
    "manifest.json",
    "verify.py",
    "reproduce.sh",
    "evidence.jsonl"
  ],
  "verification_requirements": [
    "manifest_schema_valid",
    "required_artifacts_present",
    "json_and_jsonl_parse",
    "claim_identifiers_unique",
    "evidence_identifiers_unique",
    "evidence_references_resolve",
    "source_revision_matches_checkout",
    "independent_fixtures_pass",
    "reproduction_exit_code_zero"
  ],
  "promotion": {
    "reproduction_verified": false,
    "proof_reviewed": false,
    "publication_approved": false
  }
}
```

Integration requirement: this is a proposed fail-closed manifest contract, not a verified drop-in replacement for the existing verifier's expected schema. The placeholder revision must be replaced with the actual pinned commit. The manifest must not be generated automatically to conceal a missing source artifact.

### `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/evidence.jsonl`

Deliverable — corrected evidence classification

Replace the misleading `EV-JS-002` record with the following line, after checking the current evidence registry and preserving its actual claim relationship.

```json

{"evidence_id":"EV-JS-002","claim_id":"JS-11","class":"[V]","type":"structural-package-validation","artifact":"verify.py","status":"IMPLEMENTED_STRUCTURAL_ONLY","description":"Validates package structure, JSON/JSONL parsing, identifier uniqueness, and claim/evidence references. This evidence does not establish the JOIN-STABILITY theorem and does not independently verify the declared finite fixtures."}
```

Important: `[V]` here denotes a verifier artifact, not a theorem verified. If `JS-11` asserts the mathematical theorem, its association with this evidence must be removed or supplemented with appropriate proof evidence. Do not leave the record implying that structural checks establish the theorem.

### `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/PROOF-OBLIGATIONS.md`

Deliverable — mathematical statement and proof

### JOIN-STABILITY: Finite Unary-Algebra Join Closure

Research note · 8 October 2026

### Claim

Let be a finite set, let , and let be an equivalence relation on . Define

T^{-1}(E)=\\{(x,y)\\in X^2:(T(x),T(y))\\in E\\}.

If

T^{-1}(E)\\subseteq E,

then

T^{-1}(E)=E.

Consequently, is a congruence of the unary algebra , and the induced map on is a permutation.

### Proof of the finite-set lemma

Let be the set of equivalence classes.

The hypothesis implies that if and belong to distinct -classes, then and belong to distinct -classes. Otherwise, would imply .

For each source class , let be the set of target -classes intersecting . Each is nonempty. The sets are pairwise disjoint: a target class intersecting both and would contradict the preceding implication when .

There are nonempty, pairwise disjoint subsets of a set of size . Therefore every contains exactly one class. Thus each source class maps entirely into a single target class, establishing forward preservation:

x\\mathrel E y\\implies T(x)\\mathrel E T(y).

Hence . Together with the hypothesis, this yields equality. The induced map on the quotient classes is surjective and therefore bijective.

### Join-stability theorem

Let and be equivalence relations satisfying

T^{-1}(E)\\subseteq E,\\qquad
T^{-1}(F)\\subseteq F.

By the finite-set lemma, both are congruences of . The join , meaning the least equivalence relation containing both, is also a congruence: any finite chain of \- or -related pairs remains related after applying .

Therefore,

T^{-1}(E\\vee F)=E\\vee F,

and in particular,

\\boxed{T^{-1}(E\\vee F)\\subseteq E\\vee F.}

This establishes join closure mathematically, subject to the stated definitions. The argument is a proof from the finite-set lemma and the standard congruence-join construction; it does not establish that the repository's current verifier implements or checks this proof.

### Required independent checks

* Test the finite-set lemma exhaustively for all maps and equivalence relations through a declared small-state bound.

* Test join closure independently, using a separate implementation of equivalence closure and join.

* Include negative fixtures violating the hypothesis, so the verifier demonstrates that it can reject invalid inputs.

* Verify the exact fixture inventory and expected outputs against independently derived results.

* Keep mathematical proof review separate from executable fixture verification.

Status: The mathematical argument above is supplied inline. Repository integration, independent execution, fixture results, and reproduction remain unverified.

### `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/REPRODUCTION-STATUS.md`

Deliverable — current blocker record

### JOIN-STABILITY: Reproduction and Evidence Status

Audit date · 8 October 2026

| Item                  | Status                                                             | Required action                                                                 |
| --------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| manifest.json         | Missing in the inspected audit                                     | Restore a revision-pinned manifest consistent with the verifier's actual schema |
| claims.jsonl          | Returned 404 during connected-file retrieval                       | Confirm presence or absence at the pinned commit                                |
| verify.py             | Structural checks only, according to the inspected implementation  | Separate structural validation from mathematical and fixture verification       |
| evidence.jsonl        | EV-JS-002 overstates verification scope                            | Correct the evidence description and reconcile its claim association            |
| reproduce.sh          | Not successfully reproduced in this audit                          | Run after required artifacts are restored                                       |
| Mathematical proof    | Proof argument supplied above; repository integration not verified | Review the committed proof and reconcile it with the claim registry             |
| Publication/promotion | Blocked                                                            | Do not promote based on structural validation alone                             |

### Acceptance gate

The workstream is not reproducible until the required files exist at the pinned revision, the verifier runs against that exact checkout, independent fixtures pass, and the reproduction command exits successfully. Missing artifacts must cause failure rather than silent regeneration.

No successful reproduction, test run, repository modification, or commit is claimed in this deliverable.

These are the inline artifacts for the JOIN-STABILITY workstream. The manifest is a proposed contract; the proof is a mathematical deliverable; the evidence correction and status note identify the repository repairs needed before reproducibility can be claimed.
Worked for 48s

### 1\. Exact repository actions required

A. Restore a valid JOIN-STABILITY manifest

Required path

`AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/manifest.json`

The repository's own README declares this manifest authoritative. My GitHub history query returned no commits for this exact path, so I cannot recover an earlier version from that history query. Do not fabricate a replacement schema; define the schema against the existing package contract.

Affected files

`AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/README.md` `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/reproduce.sh` `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/verify.py`

B. Correct the evidence-class mismatch

Exact file

`AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/evidence.jsonl`

Record `EV-JS-002` labels `verify.py` as `[V]` computational verification. But the live verifier explicitly says mathematical verification has not yet been added; it checks package structure and claim/evidence references.

Required correction: either implement the declared mathematical check and test it, or downgrade that evidence record to accurately describe the current implementation. Do not label a structural package check as mathematical verification.

### 2\. What the existing verifier actually establishes

File: `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/verify.py`

Its current successful path checks:

* Required files and directories exist.

* JSON and JSONL records parse.

* Claim and evidence IDs are unique.

* Evidence records reference existing claims.

It does not independently establish the JOIN-STABILITY theorem. The source code says so explicitly. This is a good separation of concerns in principle, but the evidence record must match the implementation.

I have not run the repository's code in a local execution environment during this audit. The reproduction failure above follows from the live file tree and the explicit manifest check in `reproduce.sh`; it is not a claimed test execution.

### 3\. CI status — scoped correctly

The latest workflow returned by the repository's Actions API was AQARION Mobile Research Kit Validation, run on 8 October 2026, with conclusion `success`. [View the workflow run](https://github.com/quantarion369-arch/AQARION/actions/runs/37709152608).

That is evidence for the Mobile Research Kit workflow only. It does not establish that JOIN-STABILITY reproduces successfully.

### 4\. Literature boundary

Two relevant sources reinforce the need to keep the mathematical claim narrow:

* Jakubíková-Studenovská and Janičková, [Congruence lattices of connected monounary algebras](https://doi.org/10.1007/s00012-020-00686-2), Algebra Universalis 81, article 54 (2020). This establishes relevant prior work on congruence lattices of unary algebras.

* Syrovatskaya, [Monounary algebras with periodic endomorphism semigroups](https://doi.org/10.4213/dm1886), Diskretnaya Matematika 38(1) (2026), 121–134. This is a recent related source on finite unary algebras and periodic endomorphism semigroups.

These sources do not, by themselves, settle the novelty of AQARION's particular theorem or its evidence pipeline. That comparison remains open.

### 5\. Current disposition

| Item                               | Audit result                                          |
| ---------------------------------- | ----------------------------------------------------- |
| Live repository and default branch | Inspected                                             |
| JOIN-STABILITY manifest            | Missing                                               |
| JOIN-STABILITY reproduction        | Blocked by missing manifest                           |
| Mathematical verification label    | Needs correction or implementation                    |
| Mobile Research Kit CI             | Success; different workflow                           |
| PB-CORE-004 paper proof            | Present in repository; Lean remains open per artifact |
| Literature novelty                 | Open                                                  |
| Repository modifications by me     | None                                                  |

The one task I recommend you perform first: fix the JOIN-STABILITY manifest/verifier contract. Then rerun `AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY/reproduce.sh` and preserve its actual output. Do not promote the claim based on that run unless the mathematical verification and its evidence record genuinely support the promotion.

No new identifiers, folders, or architectural layers are needed for this repair.
Worked for 3m 7s

### 2\. File: `burnside_m3_validation.md`

Action: replace the entire file. This is the cleaned, complete version; it deliberately does not claim a fresh run occurred.

# Burnside M3 Validation — AQ-BURNSIDE-M3-001

**Directory:** `AQARION-QUANTARION-AI/evidence/BURNSIDE/M3/`

**Primary record:** `burnside_m3.json`

**Recomputation program:** `burnside_m3_recompute.py`

**Hash manifest:** `burnside_m3_hashes.txt`

## 1. Mathematical statement

Let \(C(\lambda)\) be the number of set partitions fixed by a permutation with cycle type \(\lambda\), and let \(m_j\) be the multiplicity of cycles of length \(j\) in \(\lambda\). Define

\[
z_\lambda=\prod_{j\geq1}j^{m_j}m_j!.
\]

The third Burnside moment is

\[
M_3(k)=\frac{1}{k!}\sum_{\sigma\in S_k}C(\sigma)^3
=\sum_{\lambda\vdash k}\frac{C(\lambda)^3}{z_\lambda}.
\]

The second equality follows by grouping permutations by cycle type, because the conjugacy class of type \(\lambda\) has size \(k!/z_\lambda\). Burnside's lemma also identifies \(M_3(k)\) as the number of orbits of the diagonal action of \(S_k\) on ordered triples of set partitions. Thus \(M_3(k)\) must be a nonnegative integer.

## 2. Current record and known discrepancy history

The current JSON record contains the corrected integers for \(1\leq k\leq31\), including the previously disputed entries at \(k=25,27,28,29,30\). The correction history is not itself proof of a fresh execution: the stored values must be compared with a run of the checked-in program against the checked-in JSON.

A previous validation document had been concatenated with an older specification containing ellipses and malformed formula placeholders. This replacement removes that conflicting appended text.

## 3. Reproduction command

Run from this directory:

```sh
python3 burnside_m3_recompute.py
```

The program reads `burnside_m3.json` by default, performs direct permutation-level controls for \(k\leq5\), compares direct invariant-partition counts against the cycle-type recurrence for every cycle type through \(k=6\), and recomputes the cycle-type third moment for \(1\leq k\leq31\). Any mismatch exits nonzero.

## 4. Evidence interpretation

The script's success messages are outputs of the validation program; they are not proof that a run occurred merely because they appear in a file or prior conversation. A current run should be captured together with:

- The repository commit SHA used for the run.
- SHA-256 of `burnside_m3.json`, `burnside_m3_recompute.py`, and this validation document.
- The exact stdout and exit code.
- The Python version and execution environment.

The hash manifest binds file bytes; it does **not** authenticate a run, prove mathematical correctness by itself, or establish implementation independence. The direct small-domain controls and the cycle-type computation are separate checks, but they share the same program and are not a fully independent external reproduction.

## 5. Status boundary

- **Stored integer sequence:** corrected values are present in the current JSON record.
- **Fresh execution authenticated to current source revision:** PENDING.
- **Formalization:** OPEN.
- **Promotion:** BLOCKED.

Do not promote the evidence until a fresh run is recorded against the exact source revision and its outputs are reviewed. A computational pass does not imply Lean/formal verification, independent external reproduction, or proof of any broader claim beyond the stated finite domain.

### 3\. File: `burnside_m3_hashes.txt`

Action: create this missing file only after the validation document has been replaced with the exact contents above. These SHA-256 values were calculated from the fetched JSON and Python script bytes, plus the exact replacement validation text above.

```text
# SHA-256 manifest — AQ-BURNSIDE-M3-001
# Hashes cover exact UTF-8 file bytes.
# This manifest intentionally does not hash itself.
364405a49264835884fd5e97be89e1499a0d18fb9b87c38e97e9668719b1e845  burnside_m3.json
1924b987a84b162868ad5f1c90af15bd14e573c33811d435fda11bea2f9ec35a  burnside_m3_recompute.py
4002e7a7c524228e8396cd7618f8b0172786682e7fcd5bd988587c65f43019b6  burnside_m3_validation.md
```

Important: these hashes are tied to the exact file contents fetched or specified above. If you change whitespace, line endings, or content, recompute the affected hash. The hash manifest itself does not prove the program ran.

### 4\. File: `burnside_m3.json`

Action: retain the existing JSON for now. Its stored integers at the disputed positions are already corrected. I do not recommend replacing the full evidence record until the execution and provenance fields are reconciled against the repository’s ClaimLock record. In particular, `provenance.status: BOUND` must not be interpreted as proof that a fresh execution has been authenticated.

The five corrections that must remain in the record are:

|     | Correct stored value                     |
| --- | ---------------------------------------- |
| 25  | 9209030758458199302082042010781          |
| 27  | 21164152737458354181271060616858881      |
| 28  | 1082743048110523297647521576062705103    |
| 29  | 57740206450084684434628859141458156260   |
| 30  | 3205626834037541326237961731886193129380 |

### 5\. File: `burnside_m3_recompute.py`

Action: do not replace it solely on the evidence currently available. The fetched script has a plausible exact-integer cycle-type recurrence and bounded direct controls. I have not executed the live copy in this turn, so a complete replacement would risk changing a potentially correct implementation without first identifying an implementation defect.

One tightening worth making after a successful run is an explicit divisibility check before `cycle_type_M3` returns `total // math.factorial(k)`. The Burnside identity implies exact divisibility; the checker should assert that rather than relying on integer division alone. This is a hardening improvement, not evidence that the current recurrence is wrong.

### 6\. Exact execution and acceptance procedure

From the canonical directory:

```sh
cd AQARION-QUANTARION-AI/evidence/BURNSIDE/M3
python3 burnside_m3_recompute.py
```

Accept the computational check only if the program exits with status `0` and reports all expected checks as passing. Then capture the output, the Python version, and the exact Git commit SHA. Recompute the three hashes and ensure the manifest matches the finalized files.

Do not mark the package formally verified or promote the claim based solely on this run. A stronger independent reproduction should use a separately implemented method, not merely the same recurrence in a second invocation.

### Final disposition

* Mathematical identity: supported by Burnside’s lemma and cycle-type class sizes.

* Stored numerical discrepancies: corrected in the live JSON at the five identified positions.

* Validation document: defective due to conflicting appended content; replacement supplied above.

* Hash manifest: missing in the fetched repository; complete proposed contents supplied above.

* Current program correctness: not newly established by execution in this turn.

* Repository write: attempted but denied by the connected GitHub integration; no successful commit or modification is claimed.

* Formalization: `OPEN`.

* Promotion: `BLOCKED`.

The evidence currently supports a data-transcription and evidence-governance problem, not the conclusion that the underlying recurrence or all tools are wrong. The decisive next test is a fresh run of the exact live script against the exact live JSON, bound to a recorded commit and output.

https://github.com/quantarion369-arch/AQARION

### 2\. Mathematical result: what can be established independently

For a permutation , let be the number of set partitions fixed by its action on the underlying set. Define

M_3(k)=\\frac{1}{k!}\\sum_{\\sigma\\in S_k}C(\\sigma)^3.

This has a direct orbit-count interpretation: counts the ordered triples of set partitions fixed by . Burnside's lemma therefore gives

\\boxed{M_3(k)=\\#\\bigl(S_k\\backslash\\mathcal P_k^3\\bigr)\\in\\mathbb Z_{\\ge0},}

where is the set of set partitions of a -element set.

Grouping permutations by cycle type gives

|\[\\lambda\]|=\\frac{k!}{z_\\lambda},
\\qquad
z_\\lambda=\\prod_{j\\ge1}j^{m_j}m_j!,

and is constant on each conjugacy class. Consequently,

\\boxed{
M_3(k)=\\sum_{\\lambda\\vdash k}\\frac{C(\\lambda)^3}{z_\\lambda}.
}

This establishes the formula, assuming the stated definition of . It does not certify every recorded integer through ; that still requires executing and binding the implementation and its output.

### 3\. Exact next deliverable: replace the contaminated validation document

Destination: `AQARION-QUANTARION-AI/evidence/BURNSIDE/M3/burnside_m3_validation.md`

Title: Burnside M3 Validation — AQ-BURNSIDE-M3-001

Purpose: One unambiguous validation record; separate recorded claims from an execution authenticated against the live source revision.

# Burnside M3 Validation — AQ-BURNSIDE-M3-001

**Record:** `burnside_m3.json`
**Recomputation:** `burnside_m3_recompute.py`
**Hash manifest:** `burnside_m3_hashes.txt`
**Claim:** `AQ-BURNSIDE-M3-001`

## Mathematical statement

For \(k\geq1\),

\[
M_3(k)=\frac{1}{k!}\sum_{\sigma\in S_k}C(\sigma)^3
=\sum_{\lambda\vdash k}\frac{C(\lambda)^3}{z_\lambda},
\]

where \(C(\lambda)\) counts set partitions fixed by a permutation of cycle type \(\lambda\), and

\[
z_\lambda=\prod_{j\geq1}j^{m_j}m_j!.
\]

The second equality follows by grouping permutations into conjugacy classes. The first expression is an orbit count by Burnside's lemma and is therefore a nonnegative integer.

## Recorded computation scope

- Integer domain: \(1\leq k\leq31\).
- Arithmetic: exact integer/rational arithmetic.
- Recorded direct permutation control: \(k\leq5\).
- Recorded direct cycle-type control: every cycle type for \(k\leq6\).
- Recorded cycle-type recomputation: \(k\leq31\).

These are the scopes claimed by the evidence record. They must not be represented as a newly authenticated execution unless the source revision, command, exit status, output, and artifact digests are captured together.

## Required reproduction

From this directory, run:

```sh
python3 burnside_m3_recompute.py
```

The run must independently regenerate the values, compare them with `burnside_m3.json`, and exit nonzero on any mismatch.

Required checks:

- JSON parses and satisfies the expected schema.
- Direct permutation-level \(M_3\) control passes for \(k=1,\ldots,5\).
- Direct \(C(\lambda)\) control passes for all cycle types through \(k=6\).
- Cycle-type \(M_3\) comparison passes for \(k=1,\ldots,31\).
- Exact arithmetic is used.
- Total mismatches equal zero.

## Evidence interpretation

A successful run supports computational agreement on the declared finite domain. It does not, by itself, establish a universal theorem beyond that domain, novelty, external independent reproduction, or Lean formalization.

A second implementation is not automatically independent merely because it is a different file. Independence requires a justified difference in construction or an independently specified oracle.

## Current governance

- Computational record: `COMPUTED` (recorded status)
- Execution authenticated against current revision: `PENDING`
- Formalization: `OPEN`
- Promotion: `BLOCKED`

Do not promote the claim solely because the stored JSON says `PASS`.

## Hash-manifest rule

`burnside_m3_hashes.txt` must contain SHA-256 digests of the finalized JSON, recomputation script, and this validation document. Recompute all three digests after any edit. Do not include a self-hash line in the manifest.

### 4\. Recent literature relevant to AQARION's research boundary

These papers are relevant to the methodological framing, not proof of AQARION's specific claims.

* “Discrete-time dynamical systems characterization via invariance and approximation of Koopman operators and operator-valued kernels” (published 24 March 2026). It studies Koopman-invariant observable spaces and approximation bounds that account for deterministic sampling error. This supports keeping exact finite-state closure claims separate from approximation claims.

* “Adversarial dynamical systems characterize when data-driven learning succeeds or fails” (Nature Communications, 2026). Its reported results highlight that finite-dimensional Koopman approximations can produce spurious spectral behavior rather than converge as the representation grows. That reinforces AQARION's separation of exact algebraic results from learned or truncated operator models.

* “Learning stable Koopman embeddings for identification and control” (Automatica, July 2026) studies model parameterizations with built-in stability properties. It is useful context for the future learned-operator track, but it does not establish the finite quotient or defect theorems in AQARION.

### 5\. Work order — no expansion

* Replace the contaminated Burnside validation document with the clean version above.

* Run the committed `burnside_m3_recompute.py` against the committed JSON and capture the actual result.

* Create `burnside_m3_hashes.txt` from the finalized three artifacts; verify the hashes against the committed bytes.

* Bind the resulting receipt to the exact source revision. Keep `FORMALIZATION=OPEN` and `PROMOTION=BLOCKED`.

* Only then return to the FPR literature-priority and Lean proof obligations.

Execution limitation for this response: I inspected the live repository and derived the orbit-count identity, but I did not execute the repository's Python script in this turn or commit the replacement document. The inline document is the exact proposed replacement, not a claim that GitHub has been modified.

https://github.com/quantarion369-arch/AQARION
