from typing import Literal
import sympy as sp

from .base import Chunk, BarrierLayer, MeasurementBranch, StandardGateChunk, MeasurementChunk
from .circuit_backend import CircuitBackend
from .utils import _use_notebook, _display_expr

class MeasurementCircuitBackend(CircuitBackend):
    def __init__(
        self,
        chunks: list[Chunk | BarrierLayer],
        num_qubits: int,
        simplify_on_build: bool,
        global_phase: float|sp.Expr
    ):
        super().__init__(chunks, num_qubits, simplify_on_build, global_phase)
        self.branches_at_barrier: dict[str, list[MeasurementBranch]] = {}
        self.branches_is_simplified: dict[str, bool] = {}
        
        self.final_branches = self.evolve()
        self.final_branches_is_simplified: bool = simplify_on_build

    def evolve(self) -> list[MeasurementBranch]:
        psi = sp.zeros(2 ** self.num_qubits, 1)
        psi[0] = sp.exp(sp.I * self.global_phase)
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
    
    def probabilities(self, label: str|None, simplify: bool) -> sp.Matrix:
        branches = self.branches(label, simplify)
        bit_prob_map: dict[tuple[int], sp.Expr] = {}

        for b in branches:
            key = b.measured_bits # (bit0, bit1, ..., bitN) (first -> last qubit measurement outvome)
            bit_prob_map.setdefault(key, 0)
            bit_prob_map[key] += b.prob

        keys = list(bit_prob_map.keys())
        if not keys:
            raise ValueError("No branches found at label:", label)

        # Check that all key lengths are the same
        meas_len_set = {len(k) for k in keys}
        if len(meas_len_set) != 1:
            raise ValueError("Inconsistent measurement bit lengths across branches")

        N = next(iter(meas_len_set))
        dim = 2 ** N
        probs = sp.zeros(dim, 1)

        for bits, p in bit_prob_map.items():
            bit_str = ''.join(str(bit) for bit in bits)
            index = int(bit_str, 2)
            probs[index] = sp.simplify(p) if simplify else p

        return probs
    
    def simplify(self) -> None:
        for label in self.branches_at_barrier:
            self._simplify_branches(label)
        self._simplify_branches(None)
    
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
                self._report_branches(label, simplify, use_nb, use_dirac)
        else:
            self._report_branches(label, simplify, use_nb, use_dirac)
    
    def _report_branches(self, label: str|None, simplify: bool, use_nb: bool, use_dirac: bool):
        if label is None:
            print('- Final branches:')
        else:
            print(f'- Branches at {label}:')
        branches = self.branches(label, simplify)
        for branch in branches:
            outcome = ''.join([str(bit) for bit in branch.measured_bits])
            print(f'  * Measurement outcome: {outcome}')
            print(f'    Classical bits results (clbit index: measured value): {branch.clbit_results}')
            print('    Probability:')
            _display_expr(branch.prob, use_nb, use_dirac, self.num_qubits)
            print('    Statevector:')
            _display_expr(branch.state, use_nb, use_dirac, self.num_qubits)