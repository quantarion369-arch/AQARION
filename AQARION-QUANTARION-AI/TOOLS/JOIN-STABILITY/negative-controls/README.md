# JOIN-STABILITY Negative Controls

Negative controls verify that invalid package states are rejected.

## In-memory verifier tests

`python3 verify.py --self-test-negative-controls` tests rejection of:

1. duplicate claim identifiers;
2. unresolved claim dependencies;
3. missing required claim fields;
4. unknown claim fields;
5. evidence referencing an unknown claim;
6. duplicate evidence identifiers;
7. invalid mathematical status;
8. invalid evidence class;
9. absolute package paths;
10. package-path traversal.

These tests exercise in-memory validator functions. They do not
simulate every filesystem, Git, JSON parsing, or audit-script failure.

## Additional integration tests required

Before release, add and run tests for:

- malformed manifest JSON;
- missing required artifact;
- missing required directory;
- malformed JSONL;
- malformed or stale source revision;
- a tested revision that is not a descendant of the declared baseline;
- corrupted expected audit counts;
- invalid audit input;
- altered fixture content;
- audit process failure and nonzero exit status.

## Reporting

A negative control passes only when the invalid condition is rejected
for the expected reason. An exception caused by an unrelated defect
must not be counted as a successful test.

Record the exact tested revision, command, stdout, stderr, exit code,
and source hashes.
