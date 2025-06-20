import sympy as sp
from ..base import ZeroParamGate

class HGate(ZeroParamGate):
    def matrix(self):
        return (1 / sp.sqrt(2)) * sp.Matrix([
            [1, 1],
            [1, -1]
        ])

class CHGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1/sp.sqrt(2), 1/sp.sqrt(2)],
            [0, 0, 1/sp.sqrt(2), -1/sp.sqrt(2)]
        ])
