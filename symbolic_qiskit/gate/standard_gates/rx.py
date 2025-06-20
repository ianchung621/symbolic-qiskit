import sympy as sp
from ..base import OneParamGate

class RXGate(OneParamGate):
    def matrix(self):
        theta = self.theta
        return sp.Matrix([
            [sp.cos(theta / 2), -sp.I * sp.sin(theta / 2)],
            [-sp.I * sp.sin(theta / 2), sp.cos(theta / 2)]
        ])

class CRXGate(OneParamGate):
    def matrix(self):
        theta = self.theta
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, sp.cos(theta / 2), -sp.I * sp.sin(theta / 2)],
            [0, 0, -sp.I * sp.sin(theta / 2), sp.cos(theta / 2)]
        ])