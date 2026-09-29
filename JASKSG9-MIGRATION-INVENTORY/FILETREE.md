JASKSG9-MIGRATION-INVENTORY/
│
├── repositories
│   ├── repository metadata
│   ├── default branch
│   ├── visibility
│   ├── license
│   ├── topics
│   ├── timestamps
│   ├── latest commit
│   ├── tags/releases
│   └── repository lineage
│
├── files
│   ├── path
│   ├── size
│   ├── blob SHA
│   ├── executable bit
│   └── language/type
│
├── imports
│   ├── Python
│   ├── JS/TS
│   ├── Lean
│   ├── Rust
│   ├── Go
│   ├── C/C++
│   ├── Java/Kotlin
│   ├── R
│   ├── notebooks
│   ├── shell/source
│   └── LaTeX packages
│
├── dependencies
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── package.json
│   ├── Cargo.toml
│   ├── go.mod
│   ├── lakefile.*
│   ├── lean-toolchain
│   ├── Dockerfiles
│   ├── CI dependencies
│   └── OS packages
│
├── internal_graph
│   ├── module → module
│   ├── repo → repo
│   ├── file → dependency
│   └── unresolved imports
│
├── provenance
│   ├── commit
│   ├── author
│   ├── committer
│   ├── commit date
│   ├── blob SHA
│   ├── repository
│   └── historical source
│
├── verification
│   ├── tests
│   ├── workflows
│   ├── manifests
│   ├── receipts
│   ├── schemas
│   ├── certificates
│   ├── proof artifacts
│   └── verification scripts
│
├── research lineage
│   ├── AQ identifiers
│   ├── KSG identifiers
│   ├── checkpoint IDs
│   ├── claim IDs
│   ├── theorem IDs
│   ├── receipt IDs
│   └── cross-repo references
│
└── anomalies
    ├── missing imports
    ├── missing files referenced by docs
    ├── duplicate schemas
    ├── stale paths
    ├── malformed filenames
    ├── broken package boundaries
    ├── undeclared dependencies
    ├── declared-but-unused dependencies
    └── provenance mismatches
