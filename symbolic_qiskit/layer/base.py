from dataclasses import dataclass
from typing import List
import qiskit.circuit as qcc

from ..gate import gate_to_sympy_matrix

@dataclass
class Operation:
    op: qcc.Instruction
    q_idxs: List[int]

@dataclass
class StandardGate(Operation):
    def __repr__(self) -> str:
        return f"({self.op.name}, q={self.q_idxs})"
    
    @property
    def sym_matrix(self):
        return gate_to_sympy_matrix(self.op)
    

@dataclass
class Barrier(Operation):
    def __repr__(self) -> str:
        return f"({self.op.name}, q={self.q_idxs})"

@dataclass
class Measurement(Operation):
    c_idxs: List[int]

    def __repr__(self):
        return f"({self.op.name}, q={self.q_idxs}, c={self.c_idxs})"

@dataclass
class QCLayer:
    ops: list[Operation]

@dataclass
class StandardGateLayer(QCLayer):
    ops: list[StandardGate]

@dataclass
class BarrierLayer(QCLayer):
    ops: list[Barrier]

@dataclass
class MeasurementLayer(QCLayer):
    ops: list[Measurement]
