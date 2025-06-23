import sympy as sp
from ..base import ZeroParamGate

class SXGate(ZeroParamGate):
    def matrix(self):
        return (1/2) * sp.Matrix([
            [1 + sp.I, 1 - sp.I],
            [1 - sp.I, 1 + sp.I]
        ])

class SXdgGate(ZeroParamGate):
    def matrix(self):
        return (1/2) * sp.Matrix([
            [1 - sp.I, 1 + sp.I],
            [1 + sp.I, 1 - sp.I]
        ])

class CSXGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, (1 + sp.I)/2, (1 - sp.I)/2],
            [0, 0, (1 - sp.I)/2, (1 + sp.I)/2]
        ])

class CSXdgGate(ZeroParamGate):
    def matrix(self):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, (1 - sp.I)/2, (1 + sp.I)/2],
            [0, 0, (1 + sp.I)/2, (1 - sp.I)/2]
        ])
