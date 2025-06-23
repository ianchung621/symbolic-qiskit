import sympy as sp
import qiskit.circuit as qcc
from .standard_gates import GATE_REGISTRY, BASIS_GATES

def gate_to_sympy_matrix(op: qcc.Instruction) -> sp.Matrix:
    name = op.name.lower()
    if name not in GATE_REGISTRY:
        raise NotImplementedError(f"Gate '{name}' not supported.")
    gate_class = GATE_REGISTRY[name]
    return gate_class(op).matrix()