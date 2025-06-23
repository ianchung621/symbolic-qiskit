import sympy as sp
from ..base import ZeroParamGate

class YGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [0, -sp.I],
            [sp.I, 0]
        ])

class CYGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, -sp.I],
            [0, 0, sp.I, 0]
        ])
