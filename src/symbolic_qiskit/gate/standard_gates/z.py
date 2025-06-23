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

class CCZGate(ZeroParamGate):
    def matrix(self):
        mat = sp.eye(8)
        mat[7, 7] = -1
        return mat
