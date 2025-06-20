import sympy as sp
from ..base import OneParamGate

class RYYGate(OneParamGate):
    def matrix(self):
        theta = self.theta
        cos = sp.cos(theta / 2)
        isin = sp.I * sp.sin(theta / 2)
        return sp.Matrix([
            [cos,     0,     0,  isin],
            [0,     cos, -isin,     0],
            [0,   -isin,   cos,     0],
            [isin,    0,     0,   cos]
        ])