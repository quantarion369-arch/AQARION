# AQARION Finite-Map Defect Transport Auditor

**Status:** Local self-test report says PASS. Independent sandbox validation is pending.

## Purpose

Provide an exact-rational reference implementation for checking the finite-map defect operator

$$D_\Pi=(I-P_\Pi)KP_\Pi$$

and the support–rank identity

$$\operatorname{rank}(D_\Pi)=k-c(H_M).$$

## Convention

The Koopman operator is the pullback $Kf=f\circ T$. Its matrix is defined by $K[x,T(x)]=1$. The transport matrix uses source blocks as rows and target blocks as columns:

$$M_{ij}=\#\{x\in B_i:T(x)\in B_j\}.$$

## Run

`python defect_auditor.py --self-test --output fresh-output.json`

For custom input, provide a JSON file with `T` and `partition`:

`python defect_auditor.py input.json`

## Validation boundary

The program checks exact finite instances. It is not a proof assistant certificate. Independent source review, clean-sandbox reproduction, input validation and genuine implementation-mutation tests remain required before the artifact is considered independently validated. No Lean or publication status is implied.
