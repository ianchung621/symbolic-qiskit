from dataclasses import dataclass, field
from typing import List, Tuple, Dict

import sympy as sp
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
    label: str

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

    @property
    def is_collapsed(self) -> bool:
        return len(self.ops) > 1
    
    @property
    def label(self) -> str:
        return self.ops[0].label

    def __repr__(self):
        if self.is_collapsed:
            return f"BarrierLayer(label = {self.label}) (collapsed {len(self.ops)} barriers, only use the first barrier label)"
        else:
            return f"BarrierLayer(label = {self.label})"

@dataclass
class MeasurementLayer(QCLayer):
    ops: list[Measurement]

@dataclass(frozen=True)
class MeasurementBranch:
    measured_bits: Tuple[int, ...]
    prob: sp.Expr
    state: sp.Matrix
    clbit_results: Dict[int, int] = field(default_factory=dict)  # clbit_idx : measured value