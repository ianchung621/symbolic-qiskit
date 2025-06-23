import sympy as sp
from ..base import OneParamGate

class PhaseGate(OneParamGate):
    def matrix(self):
        lam = self.theta
        return sp.Matrix([
            [1, 0],
            [0, sp.exp(sp.I * lam)]
        ])

class CPhaseGate(OneParamGate):
    def matrix(self):
        lam = self.theta
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, sp.exp(sp.I * lam)]
        ])
