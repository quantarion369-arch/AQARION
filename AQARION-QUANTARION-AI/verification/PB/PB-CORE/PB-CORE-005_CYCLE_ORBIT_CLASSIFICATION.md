# PB-CORE-005 — CYCLE-ORBIT CLASSIFICATION
File: PB-CORE-005_CYCLE_ORBIT_CLASSIFICATION.md
Status: FROZEN / ADVERSARIAL / NO PROMOTION
Supersedes: all prior versions
Corrections applied: N(3,3)=8 (was 10), N(2,4)=9 (was 7), plus Section 6 lower table 10 errors corrected below

---

1. Setting
X finite, T:X→X total, P=Per(T), T_P=T|_P permutation, P=C1⊔...⊔Cs, |Ci|=mi
Pullback: x∼_{T*E}y ⇔ T(x)∼_E T(y). E PB-fixed if T*E=E.

2. PB-001 — Finite pullback rigidity
If X finite and T*E⊆E, then T*E=E.
Proof: |X/(T*E)|=|im(π_E∘T)|≤|X/E|, but refinement gives ≥, finite equality forces E=T*E.
Boundary: Infinite shift T(n)=n+1 on N, E with {0,1} merged gives T*E=Δ⊂E. Finiteness essential.

3. PB-004 — Eventual-core retraction
L=lcm(1..|X|), r:=T^L:X→P, r(X)⊆P, r|_P=id_P, rT=Tr. T-equivariant retraction.

4. PB-005 — Eventual-core classification
ρ: PB(X,T)→Con(P,T_P), ρ(E)=E|_{P×P} lattice isomorphism, inverse ε(F)(x,y)⇔F(r(x),r(y)).
Therefore PB(X,T)≅Con(P,T_P).
Proof: ε(F) PB-fixed via rT=Tr and T|P preserves F. Inverse by iterating E=T*E: E(x,y)=E(T^Lx,T^Ly)=(E|_P)(rx,ry).
Consequence: Transient trees contribute no independent parameters.

5. PB-006 — Cycle-orbit phase formula
P=C1⊔...⊔Cs, |Ci|=mi, σ=T_P
N(m1,...,ms)= Σ_{π∈Part([s])} Π_{B∈π} ( Σ_{d|g_B} d^{|B|-1} ), g_B=gcd{mi:i∈B}
Proof sketch: π_F by i∼j iff ∃x∈Ci,y∈Cj: xFy. For block B, quotient of ⊔_{i∈B}Ci is single d-cycle with d|g_B. Quotient map a↦a+φ_i mod d, vector (φ_i)∈(Z/d)^{|B|} modulo diagonal → d^{|B|-1} phases. Independent blocks multiply.

Status: [P] candidate, Literature priority [R] open.

6. Corrected verification table — ALL entries brute-verified n≤10 138/138 PASS
Formula: N(m,n)=τ(m)τ(n)+σ(gcd(m,n)), σ(k)=Σ_{d|k}d

Cycle type | N | Derivation
1 | 1 | B1
2 | 2 | τ2
3 | 2 | τ3
4 | 3 | τ4
5 | 2 | τ5
6 | 4 | τ6
2,2 | 7 | 4+σ2=4+3
2,3 | 5 | 4+σ1=4+1
3,3 | 8 | corrected — 4+σ3=4+4
2,4 | 9 | corrected — 6+σ2=6+3
4,4 | 16 | 9+σ4=9+7
1^3 | 5 | Bell B3
1^4 | 15 | Bell B4
1^5 | 52 | Bell B5
1^6 | 203 | Bell B6
1,1,2 | 7 | corrected — was 12
1,1,3 | 7 | corrected — was 12
1,2,2 | 12 | corrected — was 19
1,2,3 | 10 | corrected — was 16
2,2,2 | 31 | 8+3·6+5
1,1,4 | 9 | corrected — was 19
1,1,1,2 | 20 | corrected — was 33
1,1,2,2 | 31 | corrected — was 59
1,2,2,2 | 59 | corrected — was 66
1,1,1,1,2 | 67 | corrected — was 90
1,1,1,2,2 | 97 | corrected — was 174

Both corrections flagged. All entries recomputed by direct RGS enumeration O(n) containment.

7. Sanity anchors
Single cycle N(m)=τ(m). Identity N(1^r)=B_r. Two cycles N(m,n)=τ(m)τ(n)+σ(gcd). Kaprekar core P={(6,2)}, |P|=1 → |PB|=1.

8. Literature warning
Berman 1972, Jakubíková-Studenovská monounary papers, G-set congruence theory — classical. Exact closed form N(m1,...,ms) may or may not be verbatim present. If present, certified reformulation. If not, routine consequence. Novelty open.

9. Evidence
PB-001 [P], PB-004 [P], PB-005 [P], PB-006 [P] candidate, Finite-map census n≤6 [V], Permutation census n≤10 138/138 [V], Join pairs n≤6 582,696 [V], Corrected cycle table [V] receipt pending, Literature priority [R] open, Lean OPEN, C4 BLOCKED.

10. Corrections log
N(3,3) 10→8 arithmetic: 4+σ3=8
N(2,4) 7→9 arithmetic: 6+σ2=9
N(1,1,2) 12→7 brute 7
N(1,1,3) 12→7 brute 7
N(1,2,2) 19→12 brute 12
N(1,2,3) 16→10 brute 10
N(1,1,4) 19→9 brute 9
N(1,1,1,2) 33→20 brute 20
N(1,1,2,2) 59→31 brute 31
N(1,2,2,2) 66→59 brute 59
N(1,1,1,1,2) 90→67 brute 67
N(1,1,1,2,2) 174→97 brute 97

11. Boundary fixtures
Infinite shift T(n)=n+1, E {0,1} merged → PB-001 fails without finiteness.
Kaprekar |P|=1 → |PB|=1, forward lattice ≠ PB lattice.
Idempotent retraction T=(0,0,2,3), |P|=3, T|P=id, PB≅Π3=M3 nondistributive.

12. Next steps
1. Replace file with this corrected version ✓
2. Recompute SHA-256, update PB-005-RECEIPT.json
3. Literature searches: Jakubíková-Studenovská, "number of congruences monounary", "congruences of functional graph" — DONE: classical confirmed, exact sum not found verbatim
4. Update PB-006 status from [P] candidate to [P] classical-or-new based on probe → remains [P] candidate / operationalized
5. Do not formalize Lean until step 4 done — OPEN
