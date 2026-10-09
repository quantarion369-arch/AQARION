AQ-SM003 — GitHub Actions Verification Evidence Record

Record type: CI verification evidence
Status: "PASS — COMPUTATIONAL VERIFICATION ONLY"
Tested commit: "78f4184d9576e40c7312f6bbea1eda1bcbd0bf4e"
GitHub Actions run: "37998843745"
Job ID: "114051659524"
Artifact ID: "11648112731"

1. Run Identification

- Repository: "quantarion369-arch/AQARION"
- Workflow: ".github/workflows/sm003-verify.yml"
- Run: https://github.com/quantarion369-arch/AQARION/actions/runs/37998843745
- Result: Success
- Execution environment: GitHub-hosted Linux x86_64 runner
- Python: CPython 3.12.15
- Arithmetic: Exact rational arithmetic using Python's "fractions.Fraction"
- External Python dependencies: None reported; standard library only

2. Regression Results

Check| Recorded result
Regression tests passed| 14
Regression test failures| 0
Regression test errors| 0
Regression test skips| 0
Baseline census mismatches| 0
Map-partition pairs checked| 3,984
Overall workflow| PASS

Census by state-space size

n| Maps| Map-partition pairs| Baseline mismatches
1| 1| 1| 0
2| 4| 8| 0
3| 27| 135| 0
4| 256| 3,840| 0
Total| 288| 3,984| 0

These results establish the recorded finite census result for the tested implementation and range. They do not, by themselves, establish a universal theorem.

3. Mutation Checks

The run reported the following outcomes:

Mutation identifier| Count| Outcome
"D:(I-P)K"| 1,016| DETECTED
"D:(I-P)K^T"| 1,541| DETECTED
"D:KP(I-P)"| 2,148| DETECTED
"D:K^T"| 1,383| DETECTED
"D:PKP"| 1,836| DETECTED
"D:[K,P]"| 1,335| DETECTED
"R:c"| 2,796| DETECTED
"R:first"| 2,148| DETECTED
"R:ignore-isolated"| 1,666| DETECTED
"R:k-c-1"| 3,984| DETECTED
"R:preimage"| 1,666| DETECTED
"R:c-only-variant"| —| INVALID_MUTANT

"INVALID_MUTANT" identifies a mutation that duplicates another mutation and is not counted as an independent mutation check.

Terminology note: The generated mutation report contains legacy wording using “kill” terminology. That wording should be corrected in the source report generator, and a subsequent CI run should verify the revised report. This historical run's artifact must remain an unchanged record of what it actually produced.

4. Artifact Integrity

Downloaded CI artifact archive

- Artifact ID: "11648112731"
- Archive SHA-256:

"82d1721c57013e97b8d3f0a515dd3f77ad2384e3a4758c83b9882c947084039a"

Receipt JSON SHA-256

"b0bbcacc86cf5f4a1c4127495db3d2bac109977fd4c6909e97151f7fc38b970f"

Mutation report JSON SHA-256

"1fb8372e03f50cb22278bda84d23c31fe33c40064192c579016b5f80f352a833"

Test stderr SHA-256

"24f6d7d1d12cd6a5de105f9b078c23cb229040c95e6bd0d06dd53a07a44827dc"

The recorded hashes identify the inspected artifacts. Hash integrity alone does not establish mathematical correctness or independent certification.

5. Source File Hashes

The CI receipt recorded these source hashes:

Source file| SHA-256
"AQARION-QUANTARION-AI/verification/SM/SM003/README.md"| "d6052ff237c3edd58610d4b102724e75fc90d09e3a50a25de4ed5ba42f1f082e"
"AQARION-QUANTARION-AI/verification/SM/SM003/manifest.json"| "a3a45efa530b1cd0b41ec4b023a4add4a7b4afe45c4fb83bf22700a071de4476"
"AQARION-QUANTARION-AI/verification/SM/SM003/mutations.py"| "7fae0d2e4822b92edaeddf3a5f4e559e28bdd5ce0fba7b6049068489dcc24a22"
"AQARION-QUANTARION-AI/verification/SM/SM003/test_sm003.py"| "0ba6f4bf06f6566371dfd3e444b28fc3da0ba001bbbf0779ad84d8d8cee0ad10"

These hashes refer to the source files used by the recorded run, not necessarily to files at the repository's current HEAD.

6. Evidence Classification and Limitations

This record documents a successful finite computational verification run.

It does not claim:

- a Lean proof or successful "lake build";
- a universal mathematical theorem established solely by the census;
- independent certification of the verifier;
- verification of commits other than the tested commit;
- successful verification of the proposed mutation-report terminology correction.

The appropriate interpretation is:

CI workflow PASS; 14 regression tests passed; 3,984 finite map-partition pairs checked with zero baseline mismatches; mutation outcomes recorded; universal proof and independent certification not established by this run.

7. Follow-up Required

1. Correct the mutation report generator's legacy “kill” terminology, using "DETECTED", "NOT_DETECTED", "NOT_RUN", and "INVALID_MUTANT" as appropriate.
2. Run the existing SM003 workflow again after the source correction.
3. Inspect the new artifact and confirm the generated report contains no prohibited legacy terminology.
4. Record the new commit, run ID, artifact ID, and hashes separately. Do not modify this historical evidence record to imply the later run occurred.
