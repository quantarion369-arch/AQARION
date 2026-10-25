# Deterministic browser race evidence

## Result

User-executed browser run: 12 baseline cases passed.
Expected negative control passed: removing the search-generation guard
from a test-only page caused the stale-query assertion to fail.

## Method

The actual committed application page ran in a browser srcdoc iframe.
A controlled fetch fixture delivered synthetic responses in specified orders.
The fixture intentionally ignored abort signals.

This is not an independent replay, a real-network congestion test,
a universal race-safety guarantee, or verification of source content.

## Initial harness failure

The initial run failed during fixture initialization.
Its URL constructor used the srcdoc location as a relative-URL base.
The corrected harness uses document.baseURI and submits through the
verified form. Both drivers and both run receipts are preserved.

The initial failures are not classified as application race defects.

## Scope

The twelve cases cover startup source-list completion, query changes,
source changes, Claims mode, competing search/source-view actions,
source changes during JSON decoding, and stale HTTP/JSON errors.

Application files were not changed. Package tests were not rerun.
The harness is a standalone browser check, not an automatic pytest test.
