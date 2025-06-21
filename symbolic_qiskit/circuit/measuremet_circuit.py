import sympy as sp

from .base import Chunk, BarrierLayer, MeasurementBranch
from .circuit_backend import CircuitBackend

class MeasurementCircuitBackend(CircuitBackend):
    def __init__(self, chunks: list[Chunk | BarrierLayer], num_qubits: int):
        super().__init__(chunks, num_qubits)

    def branches(self, label: str) -> list[MeasurementBranch]:
        ...
