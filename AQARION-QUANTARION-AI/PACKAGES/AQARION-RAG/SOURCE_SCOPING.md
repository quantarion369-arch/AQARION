# Source-scoped retrieval and pinned-source navigation

## Scope

This feature adds exact manifest source selection to the existing
retrieval path. Ranking, tokenization, normalization, paragraph splitting,
and corpus contents are unchanged.

Missing source selection retains global retrieval.
Blank, repeated, whitespace-padded, and unknown selectors fail before
retrieval. Scoped candidates and expanded context remain bound to the
selected path and revision.

## API

- Existing search routes accept optional source_id.
- GET /api/sources lists validated pinned manifest entries.
- GET /api/sources/view requires source_id and returns complete pinned text.
- A missing Git object does not fall back to a working-tree file.
- Source selectors are opaque identifiers resolved against the manifest.

Source selection is a retrieval constraint, not an authorization system.

## Browser

- Global search remains the default.
- Users can select a pinned source for passage/context retrieval.
- Open complete source is a separate navigation action.
- Claims search does not consume the source selector.
- Related registry evidence remains separate and may cite other sources.
- Existing request-generation and abort handling are reused.
- Retrieved text is displayed as text, not interpreted as instructions.

## Reported validation

- Genuine pre/post global function and HTTP output equality: PASS.
- Ten focused boundary checks: PASS.
- Real temporary Git revisions of the same path: tested.
- Selected-only loading and citation reconstruction: tested.
- Missing pinned Git object without working-tree fallback: tested.
- Permanent backend and static UI regressions added.
- Final supplied package result: 119 tests and 10 subtests passed.

The scoped evidence test mocks relationship enrichment at its boundary.
Existing package tests separately exercise relationship behavior.

## User-reported browser checks

Confirmed through supplied browser output:

- Global retrieval.
- Quadratic witness selected-source retrieval.
- Claim-registry search.
- Complete quadratic witness source viewing.

Selected witness revision:
e9322761a2525a2b5fb9a0c9d31888de092d7140

Source-change clearing and disabled-control appearance were not separately
confirmed by supplied browser output.
Static checks are not browser execution or deterministic race tests.

## Limitations

Source restriction does not establish answerability or claim truth.
The selected query can still rank introductory material above results.
Complete-source viewing provides navigation, not automatic adjudication.
No independent security guarantee or model-obedience result is claimed.

## Preserved evidence

tests/receipts/source_scope contains patch drivers, recorded test output,
global before/after snapshots, and file hashes.
Patch drivers are historical implementation records, not startup scripts.

The DEFECT research collection and Hugging Face model are unchanged.
