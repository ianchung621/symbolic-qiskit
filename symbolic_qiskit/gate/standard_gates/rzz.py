import sympy as sp
from ..base import OneParamGate

class RZZGate(OneParamGate):
    def matrix(self):
        theta = self.theta
        exp_pos = sp.exp(sp.I * theta / 2)
        exp_neg = sp.exp(-sp.I * theta / 2)
        return sp.Matrix([
            [exp_neg, 0,       0,       0],
            [0,       exp_pos, 0,       0],
            [0,       0,       exp_pos, 0],
            [0,       0,       0,       exp_neg]
        ])