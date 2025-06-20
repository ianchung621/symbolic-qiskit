import sympy as sp
from ..base import ZeroParamGate

class IGate(ZeroParamGate):

    def matrix(self):
        return sp.eye(2)