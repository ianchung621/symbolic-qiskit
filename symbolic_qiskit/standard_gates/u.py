import sympy as sp
from .base import OneParamGate, TwoParamGate, ThreeParamGate
from .utils import sp_exp_i

class UGate(ThreeParamGate):
    def matrix(self):
        theta, phi, lam = self.theta, self.phi, self.lam
        return sp.Matrix([
            [sp.cos(theta / 2), -sp_exp_i(lam) * sp.sin(theta / 2)],
            [sp_exp_i(phi) * sp.sin(theta / 2), sp_exp_i(phi + lam) * sp.cos(theta / 2)]
        ])

class U1Gate(OneParamGate):
    def matrix(self):
        theta = self.theta
        return sp.Matrix([
            [1, 0],
            [0, sp_exp_i(theta)]
        ])

class U2Gate(TwoParamGate):
    def matrix(self):
        phi, lam = self.theta, self.phi
        return (1 / sp.sqrt(2)) * sp.Matrix([
            [1, -sp_exp_i(lam)],
            [sp_exp_i(phi), sp_exp_i(phi + lam)]
        ])

class U3Gate(ThreeParamGate):
    def matrix(self):
        theta, phi, lam = self.theta, self.phi, self.lam
        return sp.Matrix([
            [sp.cos(theta / 2), -sp_exp_i(lam) * sp.sin(theta / 2)],
            [sp_exp_i(phi) * sp.sin(theta / 2), sp_exp_i(phi + lam) * sp.cos(theta / 2)]
        ])

class CUGate(ThreeParamGate):
    def matrix(self):
        theta, phi, lam = self.theta, self.phi, self.lam
        cos = sp.cos(theta / 2)
        sin = sp.sin(theta / 2)
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos, -sp_exp_i(lam) * sin],
            [0, 0, sp_exp_i(phi) * sin, sp_exp_i(phi + lam) * cos]
        ])

class CU1Gate(OneParamGate):
    def matrix(self):
        lam = self.theta
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, sp_exp_i(lam)]
        ])

class CU2Gate(TwoParamGate):
    def matrix(self):
        phi, lam = self.theta, self.phi
        return (1 / sp.sqrt(2)) * sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, -sp_exp_i(lam)],
            [0, 0, sp_exp_i(phi), sp_exp_i(phi + lam)]
        ])

class CU3Gate(ThreeParamGate):
    def matrix(self):
        theta, phi, lam = self.theta, self.phi, self.lam
        cos = sp.cos(theta / 2)
        sin = sp.sin(theta / 2)
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos, -sp_exp_i(lam) * sin],
            [0, 0, sp_exp_i(phi) * sin, sp_exp_i(phi + lam) * cos]
        ])

