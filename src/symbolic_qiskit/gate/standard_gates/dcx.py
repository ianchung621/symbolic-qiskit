import sympy as sp
from ..base import ZeroParamGate

class DCXGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ])
