"""Defect operator D_Pi = (I-P_Pi) K P_Pi
Proves D^2 = 0 always, D=0 iff congruence.
"""
import numpy as np
from collections import defaultdict

def projection_matrix(part):
    """P projects onto block-constant vectors (averaging). part = tuple labels"""
    n=len(part)
    blocks=defaultdict(list)
    for i,lab in enumerate(part):
        blocks[lab].append(i)
    P=np.zeros((n,n))
    for idxs in blocks.values():
        k=len(idxs)
        for i in idxs:
            for j in idxs:
                P[i,j]=1.0/k
    return P

def koopman_matrix(T):
    """K: (Kf)(x)=f(T(x)), T tuple"""
    n=len(T)
    K=np.zeros((n,n))
    for x in range(n):
        K[x, T[x]]=1.0
    return K

def defect_matrix(T, part):
    P=projection_matrix(part)
    K=koopman_matrix(T)
    I=np.eye(len(T))
    D=(I-P) @ K @ P
    return D

def is_zero_defect(T, part, tol=1e-9):
    D=defect_matrix(T, part)
    return np.allclose(D, 0, atol=tol)

def is_nilpotent_D2(T, part, tol=1e-9):
    D=defect_matrix(T, part)
    D2=D @ D
    return np.allclose(D2, 0, atol=tol)
