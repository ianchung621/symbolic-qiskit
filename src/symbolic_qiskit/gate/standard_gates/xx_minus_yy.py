import sympy as sp
from ..base import TwoParamGate

class XXMinusYYGate(TwoParamGate):
    def matrix(self):
        theta, beta = self.theta, self.phi
        cos = sp.cos(theta / 2)
        sin = sp.sin(theta / 2)
        exp_pos = sp.exp(sp.I * beta)
        exp_neg = sp.exp(-sp.I * beta)

        return sp.Matrix([
            [cos, 0, 0, -sp.I * sin * exp_neg],
            [0,   1, 0, 0],
            [0,   0, 1, 0],
            [-sp.I * sin * exp_pos, 0, 0, cos]
        ])