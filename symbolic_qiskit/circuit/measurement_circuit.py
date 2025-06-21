import sympy as sp

from .base import Chunk, BarrierLayer, MeasurementBranch, StandardGateChunk, MeasurementChunk
from .circuit_backend import CircuitBackend

class MeasurementCircuitBackend(CircuitBackend):
    def __init__(
        self,
        chunks: list[Chunk | BarrierLayer],
        num_qubits: int,
        simplify_on_build: bool,
    ):
        super().__init__(chunks, num_qubits, simplify_on_build)
        self.branches_at_barrier: dict[str, list[MeasurementBranch]] = {}
        self.branches_is_simplified: dict[str, bool] = {}
        
        self.final_branches = self.evolve()
        self.final_branches_is_simplified: bool = simplify_on_build

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
                    branches = (
                        [b.simplify() for b in current_branches]
                        if self.simplify_on_build else list(current_branches)
                    )
                    self.branches_at_barrier[label] = branches
                    self.branches_is_simplified[label] = self.simplify_on_build
        
        if self.simplify_on_build:
            current_branches = [b.simplify() for b in current_branches]
            
        return current_branches
    
    def _simplify_branches(self, label: str | None) -> list[MeasurementBranch]:
        # if not simplified yet, simplify and cache result
        # if simplified, return from cache
        if label is None:
            if not self.final_branches_is_simplified:
                self.final_branches = [b.simplify() for b in self.final_branches]
                self.final_branches_is_simplified = True
            return self.final_branches

        if not self.branches_is_simplified.get(label, False):
            self.branches_at_barrier[label] = [b.simplify() for b in self.branches_at_barrier[label]]
            self.branches_is_simplified[label] = True

        return self.branches_at_barrier[label]
    
    def branches(self, label: str| None, simplify: bool) -> list[MeasurementBranch]:
        if label is None:
            return self._simplify_branches(None) if simplify else self.final_branches
        
        if label not in self.label_to_idx:
            raise KeyError(f"Barrier label '{label}' not found. Available labels: {self.barrier_labels}")

        if label not in self.branches_at_barrier:
            raise KeyError(f"No branches recorded at barrier '{label}'. ")

        return self._simplify_branches(label) if simplify else self.branches_at_barrier[label]
    
    def simplify(self) -> None:
        for label in self.branches_at_barrier:
            self._simplify_branches(label)
        self._simplify_branches(None)
