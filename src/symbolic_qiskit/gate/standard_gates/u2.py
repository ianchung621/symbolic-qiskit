import sympy as sp
from ..base import TwoParamGate
from ..utils import sp_exp_i

class CU2Gate(TwoParamGate):
    def matrix(self):
        phi, lam = self.theta, self.phi
        return (1 / sp.sqrt(2)) * sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, -sp_exp_i(lam)],
            [0, 0, sp_exp_i(phi), sp_exp_i(phi + lam)]
        ])

class U2Gate(TwoParamGate):
    def matrix(self):
        phi, lam = self.theta, self.phi
        return (1 / sp.sqrt(2)) * sp.Matrix([
            [1, -sp_exp_i(lam)],
            [sp_exp_i(phi), sp_exp_i(phi + lam)]
        ])