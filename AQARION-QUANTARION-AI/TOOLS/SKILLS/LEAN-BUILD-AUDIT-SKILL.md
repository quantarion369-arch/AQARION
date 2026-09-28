Lean Build Audit Skill

Purpose

Audit a Lean target as a reproducible formalization artifact.

The purpose is to distinguish:

- target selection;
- dependency pinning;
- successful compilation;
- deliberate failure detection;
- incomplete proof obligations;
- formal theorem completion.

A successful build is evidence about the build. It is not automatically evidence that every intended mathematical claim has been formalized.

Inputs

- Lean project root;
- target theorem/file(s);
- pinned dependency state;
- "lakefile.toml" / "lake-manifest.json" where applicable;
- build command;
- expected success/failure conditions;
- optional negative-control modification.

Required audit sequence

1. Identify target

Record:

- project;
- exact target file;
- theorem or declaration;
- dependency revision;
- commit or repository state.

2. Establish pinned environment

Record:

- Lean version;
- Mathlib revision where applicable;
- Lake version;
- operating system;
- architecture;
- relevant package versions.

3. Clean rebuild

Run the intended build from a clean or controlled state.

Record:

- command;
- exit code;
- stdout;
- stderr;
- elapsed time.

4. Negative control

Where practical, deliberately introduce a known-invalid target or dependency state.

The expected result is failure.

The negative control tests that the build gate actually detects an invalid state.

5. Restore target

Restore the known-good target.

Rebuild.

Expected result:

SUCCESS

6. Proof-obligation audit

Search the relevant formalization for:

sorry
admit
axiom
unsafe

Each occurrence must be classified rather than silently ignored.

An occurrence outside the target theorem may be acceptable depending on project policy, but it must be documented.

Required receipt fields

project
target
commit
lean_version
mathlib_revision
lake_version
platform
architecture
build_command
build_exit_code
negative_control_command
negative_control_exit_code
restored_build_exit_code
sorry_count
admit_count
axiom_count
stdout_hash
stderr_hash
status

Status interpretation

BUILD-PASS

The specified target builds successfully.

NEGATIVE-CONTROL-PASS

The deliberately invalid target fails as expected.

REBUILD-PASS

The known-good target builds successfully after restoration.

FORMAL-PROOF-COMPLETE

Only use when the actual theorem has no prohibited unfinished obligations under the project's formalization policy.

FORMALIZATION-OPEN

The target builds, but the mathematical theorem or its supporting declarations remain incomplete.

These statuses are independent.

Important distinction

Lean builds
    !=
the theorem is proved

the theorem is proved informally
    !=
the theorem is formally verified

formal target exists
    !=
formal target is complete

Evidence status

[R] Reproducibility / formalization infrastructure.

The skill does not itself certify a Lean theorem.
