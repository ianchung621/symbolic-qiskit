import sympy as sp
from ..base import ZeroParamGate

class SGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0],
            [0, sp.I]
        ])

class SdgGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0],
            [0, -sp.I]
        ])

class CSGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, sp.I]
        ])

class CSdgGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -sp.I]
        ])
