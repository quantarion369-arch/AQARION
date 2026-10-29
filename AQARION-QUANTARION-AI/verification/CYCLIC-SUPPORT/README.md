# AQARION cyclic-support verification

Status: finite computational evidence; no promotion implied.

## Contents

This package preserves the cyclic-support, Boolean-trade, moment,
orbit, and fixed-support shortest-walk audit scripts and JSON outputs.

## Reproduce

Run from this directory with Python 3:

    python3 -m py_compile *.py
    python3 trade_structure_summary.py
    python3 trade_orbit_audit.py
    python3 cyclic_support_semantics_audit.py
    python3 fixed_support_shortest_walk_certificates.py

Run other audit scripts separately to reproduce their respective outputs.
No optimizer is used by the reconstructed fixed-support certificate checker.

## Reported cyclic-support census

The supplied semantics-audit run reports 600 distinct size-10 supports,
8 strongly connected supports, and 1 Eulerian / once-only support.
The once-only support is 6DB6.

The reported shortest-walk lengths are:
3E7C=12, 55BE=12, 5DAE=16, 6DB6=10,
75BA=16, 799E=14, 7DAA=12, D3CB=12.

## Evidence and provenance limits

The fixed-support checker in this package is a reconstruction from
certificate data supplied in the research conversation. It checks the
cyclic words, edge multiplicities, primal balance, dual inequalities,
and primal/dual equality. It is not the recovered original generator.

The original reported certificate digest was
9a4999c7693bb72aac3dc8e824ed0776f8fd279b11886dc57bb59c41c37c6d12.
The reconstructed verifier reports a different dataset digest.
These digests are not asserted to match.

Finite checks do not establish a universal theorem. Repository placement,
script PASS, and JSON hashes do not themselves confer mathematical
certification. Preserve failed runs and negative results.
