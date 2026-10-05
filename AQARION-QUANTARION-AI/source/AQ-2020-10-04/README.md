#AQ-2020-10-04 — H_AQ-001 Verifiable Package

Dated snapshot: 2026-10-04
Hypothesis: H_AQ-001 — Defect-Nilpotency + Join-Stability

This is the first runnable package in AQARION, built on A15 Android with free tools only.

What this proves

For finite deterministic system (X,T), partition Π, Koopman pullback K, block-average projection P_Π:

D_Π = (I - P_Π) K P_Π

D² = 0 always — nilpotency degree 2, proved: (I-P)P=0 ⇒ D²=0
D=0 ⇔ congruence — x~y ⇒ T(x)~T(y) ⇔ quotient well-defined
Join-stable: If E,F are T-congruences, then E ∨ F is T-congruence

This is PB_001 finite case.

Sandbox CPU verification — receipt

n=2: 4 maps, 2 partitions, 12 joins, fails=0
n=3: 27 maps, 5 partitions, 240 joins, fails=0
n=4: 256 maps, 15 partitions, 7440 joins, fails=0
D²=0: 200 random trials, fails=0

Census fix: 1+4+27+256+3125 = 3413 not 3412
Evidence: [PV] for n≤4, OPEN for n=5+
Receipt: verification/receipts/H_AQ-001_n4_receipt.json

Structure

AQ-2020-10-04/
├── aqarion/
│   ├── init.py
│   ├── defect.py      — D_Π operator, projection, Koopman
│   ├── stability.py   — congruence check, join
│   └── joins.py       — join-stability test
├── experiments/
│   └── 01_verifiable_reward/
│       └── env.py     — Verifiable reward: 0 if D=0 else 1 (reasoning-gym style)
├── tests/
│   └── test_join_stability_property.py — exhaustive property tests
└── verification/
    └── receipts/
        └── H_AQ-001_n4_receipt.json

How to run (any free sandbox)

`bash
python -m pytest tests/test_join_stability_property.py -v
or
from aqarion.defect import is_nilpotent_D2, defect_matrix
from aqarion.stability import is_congruence, join_partitions

T = (1,2,0)  # example map on X={0,1,2}
part = (0,0,1)
print(is_nilpotent_D2(T, part))  # True
print(is_congruence(T, part))
Why this is different

No learned reward model — reward is ||D||_F, machine-checkable
No floating point claims — exact finite enumeration
Receipt with hash, not screenshot
Built for RL state abstraction: stable partitions = verifiable skills

Next

n=5: 3125 maps × 52 partitions = 8.5M joins — run in distributed free sandboxes
Experiment 02: counterexample hunt to n=8
Experiment 03: D vs bisimulation metric correlation

Principle: Prove First · Verify Exhaustively · Predict Second

https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/source/AQ-2020-10-04
