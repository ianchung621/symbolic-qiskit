import sympy as sp
from ..base import ZeroParamGate

class ZGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0],
            [0, -1]
        ])

class CZGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -1]
        ])
