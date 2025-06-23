import sympy as sp
import qiskit.circuit as qcc
from abc import ABC, abstractmethod
from .utils import parse_param


class Gate(ABC):
    def __init__(self, gate: qcc.Instruction):
        self.gate = gate

    @abstractmethod
    def matrix(self) -> sp.Matrix:
        ...


class ZeroParamGate(Gate):
    def __init__(self, gate: qcc.Instruction):
        if gate.params:
            raise ValueError(f"{gate.name} expected 0 parameters, got {len(gate.params)}")
        super().__init__(gate)


class OneParamGate(Gate):
    def __init__(self, gate: qcc.Instruction):
        if len(gate.params) != 1:
            raise ValueError(f"{gate.name} expected 1 parameter, got {len(gate.params)}")
        super().__init__(gate)
        self.theta = parse_param(gate.params[0])


class TwoParamGate(Gate):
    def __init__(self, gate: qcc.Instruction):
        if len(gate.params) != 2:
            raise ValueError(f"{gate.name} expected 2 parameters, got {len(gate.params)}")
        super().__init__(gate)
        self.theta = parse_param(gate.params[0])
        self.phi = parse_param(gate.params[1])


class ThreeParamGate(Gate):
    def __init__(self, gate: qcc.Instruction):
        if len(gate.params) != 3:
            raise ValueError(f"{gate.name} expected 3 parameters, got {len(gate.params)}")
        super().__init__(gate)
        self.theta = parse_param(gate.params[0])
        self.phi = parse_param(gate.params[1])
        self.lam = parse_param(gate.params[2])

class FourParamGate(Gate):
    def __init__(self, gate: qcc.Instruction):
        if len(gate.params) != 4 and len(gate.params) != 3:
            raise ValueError(f"{gate.name} expected 3 or 4 parameters, got {len(gate.params)}")
        super().__init__(gate)
        self.theta = parse_param(gate.params[0])
        self.phi = parse_param(gate.params[1])
        self.lam = parse_param(gate.params[2])
        self.gamma = parse_param(gate.params[3]) if len(gate.params) == 4 else 0