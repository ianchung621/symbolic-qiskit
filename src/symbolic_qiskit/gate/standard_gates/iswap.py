import sympy as sp
from ..base import ZeroParamGate

class iSwapGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 0, sp.I, 0],
            [0, sp.I, 0, 0],
            [0, 0, 0, 1]
        ])
