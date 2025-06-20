import sympy as sp
from ..base import OneParamGate

class RZGate(OneParamGate):
    def matrix(self):
        lam = self.theta
        return sp.Matrix([
            [sp.exp(-sp.I * lam / 2), 0],
            [0, sp.exp(sp.I * lam / 2)]
        ])

class CRZGate(OneParamGate):
    def matrix(self):
        lam = self.theta
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, sp.exp(-sp.I * lam / 2), 0],
            [0, 0, 0, sp.exp(sp.I * lam / 2)]
        ])
