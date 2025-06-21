import sympy as sp

from .base import Chunk, BarrierLayer, MeasurementBranch, StandardGateChunk, MeasurementChunk
from .circuit_backend import CircuitBackend

class MeasurementCircuitBackend(CircuitBackend):
    def __init__(self, chunks: list[Chunk | BarrierLayer], num_qubits: int):
        super().__init__(chunks, num_qubits)
        self.branches_at_barrier: dict[str, dict[str, MeasurementBranch]] = {}
        self.final_branches = self.evolve()

    def evolve(self) -> list[MeasurementBranch]:
        psi = sp.zeros(2 ** self.num_qubits, 1)
        psi[0] = 1
        current_branches = [MeasurementBranch((), 1, psi, {})]

        for chunk, U_chunk in zip(self.chunks, self.chunk_matrices):
            
            if isinstance(chunk, StandardGateChunk):
                for i in range(len(current_branches)):
                    b = current_branches[i]
                    current_branches[i] = MeasurementBranch(
                        measured_bits=b.measured_bits,
                        prob=b.prob,
                        state=U_chunk @ b.state,
                        clbit_results=b.clbit_results
                    )
            elif isinstance(chunk, MeasurementChunk):
                current_branches = chunk.apply_measurement(current_branches)
            elif isinstance(chunk, BarrierLayer):
                label = chunk.label
                if label is not None:
                    self.branches_at_barrier[label] = current_branches
            
        return current_branches
    
    def branches(self, label: str| None) -> list[MeasurementBranch]:
        if label is None:
            return self.final_branches
        
        if label not in self.label_to_idx:
            raise KeyError(f"Barrier label '{label}' not found. Available labels: {self.barrier_labels}")

        if label not in self.branches_at_barrier:
            raise KeyError(f"No branches recorded at barrier '{label}'. ")

        return self.branches_at_barrier[label]
