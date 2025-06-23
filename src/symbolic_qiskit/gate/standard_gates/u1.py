import sympy as sp
from ..base import OneParamGate
from ..utils import sp_exp_i

class U1Gate(OneParamGate):
    def matrix(self):
        theta = self.theta
        return sp.Matrix([
            [1, 0],
            [0, sp_exp_i(theta)]
        ])

class CU1Gate(OneParamGate):
    def matrix(self):
        lam = self.theta
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, sp_exp_i(lam)]
        ])