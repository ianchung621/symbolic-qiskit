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
    def label(self) -> str | None:
        for op in self.ops:
            if op.label is not None:
                return op.label
        return None

    def __repr__(self):
        if not self.is_collapsed:
            return f"BarrierLayer(label = {self.label})"
        
        if self.label is not None:
            return f"BarrierLayer(label = {self.label}) (collapsed {len(self.ops)} barriers, only use the non-None first barrier label)"
        else:
            return f"BarrierLayer(label = None) (collapsed {len(self.ops)} barriers)"

@dataclass
class MeasurementLayer(QCLayer):
    ops: list[Measurement]

@dataclass(frozen=True)
class MeasurementBranch:
    measured_bits: Tuple[int, ...]
    prob: sp.Expr
    state: sp.Matrix
    clbit_results: Dict[int, int] = field(default_factory=dict)  # clbit_idx : measured value

    def simplify(self):
        
        new_prob = sp.simplify(self.prob)
        new_state = self.state.applyfunc(sp.simplify)

        return MeasurementBranch(
            measured_bits=self.measured_bits,
            prob=new_prob,
            state=new_state,
            clbit_results=self.clbit_results,
        )