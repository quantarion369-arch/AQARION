# Claim Audit Skill

## Purpose

Audit a mathematical claim before it is promoted, published, or attached to
a stronger evidence label.

This skill is infrastructure, not a proof engine. It records the actual
evidence boundary.

## Inputs

- claim identifier, if one exists;
- exact mathematical statement;
- definitions and hypotheses;
- source artifact(s);
- computational result(s), if any;
- formalization status, if any;
- known counterexamples, corrections, or retractions.

## Outputs

A claim-audit record containing:

1. exact statement;
2. evidence class;
3. verification domain;
4. proof status;
5. formalization status;
6. reproduction path;
7. known limitations;
8. invalidation history;
9. promotion recommendation limited to the evidence actually present.

## Evidence classes

- "[D]" Definition
- "[P]" Mathematical proof
- "[V]" Exhaustive or independently reproducible verification
- "[PV]" Proof + verification
- "[C]" Conjecture
- "[R]" Research / exploratory result
- "OPEN" Active research / unresolved
- "FROZEN" Locked for audit
- "BLOCKED" Gate prevents promotion
- "QUARANTINED" Evidence retained but excluded from promotion
- "DEPRECATED" Obsolete representation retained for provenance — was KILLED
- "SUPERSEDED" Replaced by successor
- "RETRACTED" Withdrawn due to error
- "REFUTED" Counterexample exists

Evidence classes do not upgrade automatically.

## Procedure

1. Normalize the statement.
2. List every hypothesis explicitly.
3. Separate mathematical proof from computation.
4. Record the exact finite domain for exhaustive claims.
5. Check whether the computation is independent of the producer
implementation when independence is claimed.
6. Check for negative controls when a verifier exists.
7. Check formal files for unfinished proof markers such as "sorry" or
"admit" when formal completion is claimed.
8. Search the correction/retraction ledger for superseded statements.
9. Record what the evidence does not establish.
10. Preserve the original claim text when the result is deprecated /
retracted / refuted / quarantined.

## Failure conditions

The audit must stop or downgrade the claim when:

- the statement is broader than the verified domain;
- a proof depends on an unproved lemma;
- a computation is presented as proof;
- the verifier imports the producer implementation when independence is
required;
- a negative control is expected but absent;
- formalization contains unfinished obligations while formal completion is
claimed;
- the claim conflicts with a known correction or counterexample.

## Required principle

SEARCH!= PROOF

REPRODUCED!= MINIMAL

MINIMAL!= PROVED

PROVED!= FORMALLY VERIFIED

PUBLIC!= CERTIFIED

## Evidence status

[R] Research infrastructure specification.

The skill itself does not certify any mathematical claim.

## License

Apache License 2.0 — Copyright 2026 James Aaron / quantarion369-arch / AQARION
