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