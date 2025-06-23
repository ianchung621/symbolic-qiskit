import sympy as sp
from ..base import ZeroParamGate

class XGate(ZeroParamGate):

    def matrix(self):
        return sp.Matrix([
            [0, 1],
            [1, 0]
        ])

class CXGate(ZeroParamGate):

    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])

class CCXGate(ZeroParamGate):
    def matrix(self):
        mat = sp.eye(8)
        mat[6,6] = 0
        mat[7,7] = 0
        mat[6,7] = 1
        mat[7,6] = 1
        return mat