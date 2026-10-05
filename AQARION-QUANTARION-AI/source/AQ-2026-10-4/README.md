AQ-2026-10-04 — H_AQ-001 Dated Package

Snapshot date: 2026-10-04  
Location: AQARION-QUANTARION-AI/source/AQ-2026-10-04  
Built on: A15 Android, free tools only, on/off free time  
Author: quantarion369-arch (transition from JASKSG9)

What this is

A small, runnable package for one finite theorem. No claims beyond what is tested.

Hypothesis H_AQ-001:
For finite deterministic map T:X→X, partition Π, with P_Π = block-average projection and K = Koopman pullback (Kf)(x)=f(T(x)), define

D_Π = (I - P_Π) K P_Π

What is actually shown here

D_Π² = 0 always — mathematical proof: P²=P ⇒ (I-P)P=0 ⇒ D²=(I-P)KP(I-P)KP=0. Also checked numerically for 200 random T,Π.

D_Π=0 ⇔ Π is a congruence (x~y ⇒ T(x)~T(y)). This is standard quotient criterion, implemented as is_congruence().

Join of congruences is congruence for |X| ≤ 4 — tested by exhaustive enumeration, not proved for all n.

Verification counts (run in free Python sandbox):
n=2: 4 maps, 2 partitions, 12 joins tested, 0 fails
n=3: 27 maps, 5 partitions, 240 joins tested, 0 fails
n=4: 256 maps, 15 partitions, 7440 joins tested, 0 fails

Census correction noted during this work: total deterministic maps for |X|≤5 is 1+4+27+256+3125 = 3413, not 3412.

Receipt file: verification/receipts/H_AQ-001_n4_receipt.json (or receipts/verification/ in current upload — same content)

Evidence class: [PV] for n≤4 (property verified by computation), OPEN for n≥5.

What is NOT claimed

Not a proof for all finite X — only exhaustive up to n=4.
Not a formal Lean proof — Lean formalization is future work.
Not peer-reviewed — this is a dated working snapshot.
Not a full RL library — experiments/01_verifiable_reward/env.py is a minimal example where reward = 0 if ||D||_F < 1e-9 else 1. No agent training is included here.
No claim of novelty for D²=0 — it follows from projection idempotence; included for explicit verification.

Structure in this folder

AQ-2026-10-04/
├── aqarion/
│   ├── init.py
│   ├── defect.py       — P_Π, K, D_Π
│   ├── stability.py    — is_congruence, join_partitions
│   └── joins.py        — join test helper
├── experiments/
│   └── 01_verifiable_reward/
│       └── env.py
├── tests/
│   └── test_join_stability_property.py
└── verification/
    └── receipts/
        └── H_AQ-001_n4_receipt.json

If you see defect.py and stability.py at the root of this folder, they are duplicates left from copy-paste — the canonical copies are inside aqarion/.

How to run

`bash
install dependency
pip install numpy

run property tests
python -m pytest tests/test_join_stability_property.py -v

quick manual check
python -c "from aqarion.defect import is_nilpotent_D2; print(is_nilpotent_D2((1,2,0),(0,0,1)))"
Limitations

Exhaustive enumeration is exponential — n=5 is 3125 maps × 52 partitions = ∼8.5M join checks, not run in this snapshot.
Uses floating-point averaging for P_Π — zero check uses tolerance 1e-9. Exact rational version is TODO.
No CI yet — tests were run locally in sandbox, receipt is manual.

Next steps for this package

Move receipts/verification → verification/receipts to match repo convention
Delete duplicate defect.py, stability.py at folder root
Run n=5 enumeration in distributed free sandboxes
Add requirements.txt with numpy

Principle

Prove First · Verify Exhaustively · Predict Second · No Free Parameters
