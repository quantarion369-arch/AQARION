# AQARION Evidence Ledger

Status: PLACEHOLDER — navigation stub. Content pending.

## Purpose

This ledger will record claim-level evidence: exact statement, hypotheses,
declared domain, evidence type, execution records, artifact hashes,
independent reconstruction status, and disposition.

## Currently verified claims (repository-level)

| Claim | Evidence type | Test artifact |
|---|---|---|
| rank((I-P_j)KP_j) = dim W_{j+1} - dim W_j | [V] | test_closure_profile.py |
| c_lin <= c_part | [V] | test_partition_repair.py |
| Defect-rank profile does not determine c_part | [V] + hand verification | test_profile_separation.py |
| SM003 bounded census replay | [V], clean-checkout | SM003 replay receipt |

This stub is not itself a complete evidence record. Full per-claim entries
with hashes, receipts, and scope statements are pending.
