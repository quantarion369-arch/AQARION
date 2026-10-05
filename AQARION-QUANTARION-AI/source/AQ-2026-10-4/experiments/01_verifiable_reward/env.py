"""Verifiable Reward RL env: reward = 0 if D=0 else 1
This is your reasoning-gym killer — no learned reward model.
"""
from src.aqarion.defect import defect_matrix
import numpy as np

class DefectRewardEnv:
    def __init__(self, T):
        self.T=T
        self.n=len(T)
    def reward(self, part):
        D=defect_matrix(self.T, part)
        norm=np.linalg.norm(D, ord='fro')
        return 0.0 if norm<1e-9 else 1.0
    def is_stable(self, part):
        return self.reward(part)==0.0
