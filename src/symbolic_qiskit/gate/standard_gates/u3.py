import sympy as sp
from ..base import ThreeParamGate
from ..utils import sp_exp_i

class U3Gate(ThreeParamGate):
    def matrix(self):
        theta, phi, lam = self.theta, self.phi, self.lam
        return sp.Matrix([
            [sp.cos(theta / 2), -sp_exp_i(lam) * sp.sin(theta / 2)],
            [sp_exp_i(phi) * sp.sin(theta / 2), sp_exp_i(phi + lam) * sp.cos(theta / 2)]
        ])

class CU3Gate(ThreeParamGate):
    def matrix(self):
        theta, phi, lam = self.theta, self.phi, self.lam
        cos = sp.cos(theta / 2)
        sin = sp.sin(theta / 2)
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos, -sp_exp_i(lam) * sin],
            [0, 0, sp_exp_i(phi) * sin, sp_exp_i(phi + lam) * cos]
        ])
