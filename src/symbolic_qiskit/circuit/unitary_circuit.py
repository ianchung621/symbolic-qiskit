from typing import Literal

import sympy as sp

from .base import Chunk, BarrierLayer, StandardGateChunk
from .circuit_backend import CircuitBackend
from .utils import _use_notebook, _display_expr

class UnitaryCircuitBackend(CircuitBackend):
    def __init__(
        self, 
        chunks: list[Chunk | BarrierLayer],
        num_qubits: int,
        simplify_on_build: bool,
        global_phase: float|sp.Expr
    ):
        super().__init__(chunks, num_qubits, simplify_on_build, global_phase)
        self.state_at_barrier: dict[str, sp.Matrix] = {}
        self.state_is_simplified: dict[str, bool] = {}

        self.final_state_vector = self.evolve()
        self.final_state_is_simplified: bool = simplify_on_build

    def evolve(self) -> sp.Matrix:
        psi: sp.Matrix = sp.zeros(2 ** self.num_qubits, 1)
        psi[0] = sp.exp(sp.I * self.global_phase)

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
    
    def probabilities(self, label: str|None, simplify: bool) -> sp.Matrix:
        psi = self.statevector(label=label, simplify=simplify)
        probs: sp.Matrix = psi.H.T.multiply_elementwise(psi)
        if simplify:
            probs = probs.applyfunc(sp.simplify)
        return probs
    
    def simplify(self) -> None:
        for label in self.state_at_barrier:
            self._simplify_state(label)
        self._simplify_state(None)
    
    def report(self, 
        label: Literal["*", None] | str,
        simplify: bool,
        output: Literal["auto", "terminal", "notebook"],
        notation: Literal["dirac", "column"],
    ) -> None:
        if notation not in {"dirac", "column"}:
            raise ValueError(f"Invalid notation: '{notation}'. Must be 'dirac' or 'column'.")  
        use_nb = _use_notebook(output)
        use_dirac = notation == "dirac"
        if label == "*":
            for label in [None] + self.barrier_labels:
                self._report_state(label, simplify, use_nb, use_dirac)
        else:
            self._report_state(label, simplify, use_nb, use_dirac)
    
    def _report_state(self, label: str|None, simplify: bool, use_nb: bool, use_dirac: bool):
        if label is None:
            print('- Final statevector:')
        else:
            print(f'- Statevector at {label}:')
        _display_expr(self.statevector(label, simplify), use_nb, use_dirac, self.num_qubits)
    
        
