import sympy as sp
from ..base import ZeroParamGate

class TGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0],
            [0, sp.exp(sp.I * sp.pi / 4)]
        ])

class TdgGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0],
            [0, sp.exp(-sp.I * sp.pi / 4)]
        ])

class CTGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, sp.exp(sp.I * sp.pi / 4)]
        ])

class CTdgGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, sp.exp(-sp.I * sp.pi / 4)]
        ])
