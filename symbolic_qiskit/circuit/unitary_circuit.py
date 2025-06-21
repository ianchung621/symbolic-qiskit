import sympy as sp

from .base import Chunk, BarrierLayer, StandardGateChunk
from .circuit_backend import CircuitBackend

class UnitaryCircuitBackend(CircuitBackend):
    def __init__(
        self, 
        chunks: list[Chunk | BarrierLayer],
        num_qubits: int,
        simplify_on_build: bool
    ):
        super().__init__(chunks, num_qubits, simplify_on_build)
        self.state_at_barrier: dict[str, sp.Matrix] = {}
        self.state_is_simplified: dict[str, bool] = {}

        self.final_state_vector = self.evolve()
        self.final_state_is_simplified: bool = simplify_on_build

    def evolve(self) -> sp.Matrix:
        psi: sp.Matrix = sp.zeros(2 ** self.num_qubits, 1)
        psi[0] = 1

        for chunk, U_chunk in zip(self.chunks, self.chunk_matrices):
            if isinstance(chunk, StandardGateChunk):
                psi = U_chunk @ psi
            elif isinstance(chunk, BarrierLayer):
                label = chunk.label
                if label is not None:
                    state = psi.applyfunc(sp.simplify) if self.simplify_on_build else psi
                    self.state_at_barrier[label] = state
                    self.state_is_simplified[label] = self.simplify_on_build
        return psi.applyfunc(sp.simplify) if self.simplify_on_build else psi
    
    def _simplify_state(self, label: str | None) -> sp.Matrix:
        # if not simplified yet, simplify and cache result
        # if simplified, return from cache
        if label is None:
            if not self.final_state_is_simplified:
                self.final_state_vector = self.final_state_vector.applyfunc(sp.simplify)
                self.final_state_is_simplified = True
            return self.final_state_vector

        if not self.state_is_simplified.get(label, False):
            self.state_at_barrier[label] = self.state_at_barrier[label].applyfunc(sp.simplify)
            self.state_is_simplified[label] = True
        return self.state_at_barrier[label]

    def statevector(self, label: str|None, simplify: bool) -> sp.Matrix:
        if label is None:
            return self._simplify_state(None) if simplify else self.final_state_vector

        if label not in self.label_to_idx:
            raise KeyError(
                f"Barrier label '{label}' not found. Available labels: {self.barrier_labels}"
            )
        
        return self._simplify_state(label) if simplify else self.state_at_barrier[label]
    
    def simplify(self) -> None:
        for label in self.state_at_barrier:
            self._simplify_state(label)
        self._simplify_state(None)