import sympy as sp

from .base import Chunk, BarrierLayer
from .circuit_backend import CircuitBackend

class UnitaryCircuitBackend(CircuitBackend):
    def __init__(self, chunks: list[Chunk | BarrierLayer], num_qubits: int):
        super().__init__(chunks, num_qubits)

    def statevector(self, label: str) -> sp.Matrix:
        ...

    def unitary(self, label_start: str, label_end: str = None) -> sp.Matrix:
        ...
