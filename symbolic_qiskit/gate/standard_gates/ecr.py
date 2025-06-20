import sympy as sp
from ..base import ZeroParamGate

class ECRGate(ZeroParamGate):
    def matrix(self):
        return (1 / sp.sqrt(2)) * sp.Matrix([[0, 0, 1, sp.I],
                [0, 0, sp.I, 1],
                [1, -sp.I, 0, 0],
                [-sp.I, 1, 0, 0]])