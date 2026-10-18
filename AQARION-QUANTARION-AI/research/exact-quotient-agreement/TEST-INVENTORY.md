# Session Test and Experiment Inventory

Recorded phone runs; links identify artifacts, not a fresh replay.

## 001 / Quotient agreement

3,984 map-partition cases; zero disagreements.

[Source](quotient-audit-001/quotient_audit.py) | [Report](quotient-audit-001/report.json) | [Checksums](quotient-audit-001/SHA256SUMS) | [Exit](quotient-audit-001/exit-status.txt)

## 002 / Mutation detection

144 cases; three selected implementation mistakes detected.

[Source](quotient-followup-002/mutation_audit.py) | [Report](quotient-followup-002/report.json) | [Checksums](quotient-followup-002/SHA256SUMS) | [Exit](quotient-followup-002/exit-status.txt)

## 003 / Semantic checks

144 entrywise and relabeling cases, plus projection and iteration checks.

[Source](quotient-semantic-003/semantic_audit.py) | [Report](quotient-semantic-003/report.json) | [Checksums](quotient-semantic-003/SHA256SUMS) | [Exit](quotient-semantic-003/exit-status.txt)

## 004 / Closure certificate

One exact minimal-dimension certificate; four selected corruptions rejected.

[Source](closure-certificate-004/closure_certificate.py) | [Report](closure-certificate-004/report.json) | [Checksums](closure-certificate-004/SHA256SUMS) | [Exit](closure-certificate-004/exit-status.txt)

## Synthetic DNA / Separate domain

5,460 synthetic sequences; 16,380 property checks. No biological inference.

[Source](../synthetic-reverse-complement/rc-audit-001/audit.py) | [Report](../synthetic-reverse-complement/rc-audit-001/report.json) | [Checksums](../synthetic-reverse-complement/rc-audit-001/SHA256SUMS) | [Exit](../synthetic-reverse-complement/rc-audit-001/exit-status.txt)

## Existing production closure tests

[Source](../../verification/defect-transport/test_closure_profile.py): five tests passed in the supplied terminal transcript. No dedicated run bundle was saved.

## Other local work

The 10 clip-library unit tests are inside local aqarionz.py; that utility and personal clips are not copied here. The production-to-certificate bridge was observed in terminal output only and is not yet a saved artifact.

## Reproduction

Run each Python source explicitly. Keep the quotient directories as siblings: 002 and 003 depend on 001. These scripts are not all unittest-discoverable test files.

## Boundaries

Finite checks and exact instance certificates are not universal or Lean proofs. Novelty and independent reproduction are not established. Checksums establish consistency, not authenticity.
