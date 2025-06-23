import sympy as sp
from ..base import OneParamGate

class RYGate(OneParamGate):
    def matrix(self):
        theta = self.theta
        return sp.Matrix([
            [sp.cos(theta / 2), -sp.sin(theta / 2)],
            [sp.sin(theta / 2),  sp.cos(theta / 2)]
        ])

class CRYGate(OneParamGate):
    def matrix(self):
        theta = self.theta
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, sp.cos(theta / 2), -sp.sin(theta / 2)],
            [0, 0, sp.sin(theta / 2),  sp.cos(theta / 2)]
        ])
