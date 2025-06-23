import sympy as sp
import qiskit.circuit as qcc
from .standard_gates import FULL_GATE_REGISTRY, SUPPORTED_GATES

def gate_to_sympy_matrix(op: qcc.Instruction) -> sp.Matrix:
    name = op.name.lower()
    if name not in SUPPORTED_GATES:
        raise NotImplementedError(f"Gate '{name}' not supported.")
    gate_class = FULL_GATE_REGISTRY[name]
    return gate_class(op).matrix()