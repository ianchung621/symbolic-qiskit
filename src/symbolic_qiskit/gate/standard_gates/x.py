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

class C3SXGate(ZeroParamGate):
    def matrix(self):
        mat = sp.eye(8)
        mat[7, 7] = sp.Rational(1, 2) + sp.Rational(1, 2) * sp.I
        return mat

class RCCXGate(ZeroParamGate):
    def matrix(self):
        mat = sp.eye(8)
        mat[5, 5] = -1
        mat[6, 6] = 0
        mat[7, 7] = 0
        mat[6, 7] = -sp.I
        mat[7, 6] = sp.I
        return mat

class RC3XGate(ZeroParamGate):
    def matrix(self):
        mat = sp.eye(16)
        mat[12, 12] = sp.I
        mat[13, 13] = -sp.I
        mat[14, 14] = 0
        mat[14, 15] = 1
        mat[15, 14] = -1
        mat[15, 15] = 0
        return mat