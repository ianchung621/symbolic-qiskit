import sympy as sp
from ..base import ZeroParamGate

class SwapGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])

class CSWAPGate(ZeroParamGate):
    def matrix(self):
        mat = sp.eye(8)
        mat[5, 5] = 0  # |101⟩
        mat[6, 6] = 0  # |110⟩
        mat[5, 6] = 1
        mat[6, 5] = 1
        return mat

