import sympy as sp
from ..base import TwoParamGate

class RGate(TwoParamGate):
    def matrix(self):
        theta, phi = self.theta, self.phi
        cos = sp.cos(theta / 2)
        sin = sp.sin(theta / 2)
        plus = sp.I * sp.exp(sp.I * phi)
        minus = sp.I * sp.exp(-sp.I * phi)
        return sp.Matrix([
            [cos, -minus * sin],
            [-plus * sin, cos]
        ])

class CRGate(TwoParamGate):
    def matrix(self):
        theta, phi = self.theta, self.phi
        cos = sp.cos(theta / 2)
        sin = sp.sin(theta / 2)
        plus = sp.I * sp.exp(sp.I * phi)
        minus = sp.I * sp.exp(-sp.I * phi)
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos, -minus * sin],
            [0, 0, -plus * sin, cos]
        ])