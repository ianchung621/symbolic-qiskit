import sympy as sp

from .base import Chunk, BarrierLayer, StandardGateChunk
from .circuit_backend import CircuitBackend

class UnitaryCircuitBackend(CircuitBackend):
    def __init__(self, chunks: list[Chunk | BarrierLayer], num_qubits: int):
        super().__init__(chunks, num_qubits)
        self.state_at_barrier: dict[str, sp.Matrix] = {}
        self.final_state_vector = self.evolve()

    def evolve(self) -> sp.Matrix:
        psi = sp.zeros(2 ** self.num_qubits, 1)
        psi[0] = 1

        for chunk, U_chunk in zip(self.chunks, self.chunk_matrices):
            if isinstance(chunk, StandardGateChunk):
                psi = U_chunk @ psi
            elif isinstance(chunk, BarrierLayer):
                label = chunk.label
                if label is not None:
                    self.state_at_barrier[label] = psi
        return psi

    def statevector(self, label: str|None) -> sp.Matrix:
        if label is None:
            return self.final_state_vector

        if label not in self.label_to_idx:
            raise KeyError(
                f"Barrier label '{label}' not found. Available labels: {self.barrier_labels}"
            )

        return self.state_at_barrier[label]