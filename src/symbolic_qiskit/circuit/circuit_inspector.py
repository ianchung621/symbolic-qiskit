from typing import Literal

import sympy as sp
from qiskit import QuantumCircuit

from .build import circuit_to_chunks
from .base import MeasurementChunk, MeasurementBranch, BarrierLayer
from .measurement_circuit import MeasurementCircuitBackend
from .unitary_circuit import UnitaryCircuitBackend

class CircuitInspector:
    def __init__(self, qc: QuantumCircuit, simplify_on_build: bool = False):
        chunked_circuit = circuit_to_chunks(qc)
        chunks = chunked_circuit.chunks
        globel_phase = chunked_circuit.global_phase
        
        self.has_measurement = any(isinstance(c, MeasurementChunk) for c in chunks)
        self.mode: Literal["unitary", "measurement"] = (
            "measurement" if self.has_measurement else "unitary"
        )

        if self.mode == "unitary":
            self.backend = UnitaryCircuitBackend(chunks, qc.num_qubits, simplify_on_build, globel_phase)
        else:
            self.backend = MeasurementCircuitBackend(chunks, qc.num_qubits, simplify_on_build, globel_phase)
    
    def __repr__(self):
        return f"<CircuitInspector mode={self.mode}, num_qubits={self.backend.num_qubits}, barrier_labels={self.backend.barrier_labels}, chunks={self.backend.chunks}>"

    def statevector(self, label: str|None = None, simplify: bool = False) -> sp.Matrix:
        """
        Returns the symbolic statevector at the given barrier label.

        Args:
            label (str | None): Barrier label to query.
                If None, return the final statevector of the circuit
            simplify (bool): If True, simplify the result before returning.

        Returns:
            sympy.Matrix: Statevector at the specified barrier.
        """
        if self.mode != "unitary":
            raise RuntimeError("Cannot query `statevector()` on a circuit with measurement — use `branches()` instead.")
        return self.backend.statevector(label, simplify)

    def branches(self, label: str|None = None, simplify: bool = False) -> list[MeasurementBranch]:
        """
        Returns the measurement branches (list[MeasurementBranch]) at the given barrier label.

        Each MeasurementBranch includes:
            - measured_bits: Tuple[int, ...]        # ordered measurement outcomes (0 or 1)
            - prob: sympy.Expr                      # symbolic probability of this branch
            - state: sympy.Matrix                   # symbolic post-measurement statevector
            - clbit_results: Dict[int, int]         # classical register mapping (clbit_idx -> value)

        Args:
            label (str | None): Barrier label to query.
                If None, return the final branches of the circuit
            simplify (bool): If True, simplify each branch before returning.

        Returns:
            list[MeasurementBranch]: branches at the specified barrier.
        """
        if self.mode != "measurement":
            raise RuntimeError("Circuit has no measurements — use `statevector()` instead.")
        return self.backend.branches(label, simplify)
    
    def probabilities(self, label: str|None = None, simplify: bool = False) -> sp.Matrix:
        """
        Return symbolic measurement probabilities as a column vector.

        ⚠️ IMPORTANT: The index meaning depends on the circuit mode:

        - In **unitary mode**, output Matrix index refers to **qubit order** in circuit:
            [qubit_{n-1}, ..., qubit_0].

        - In **measurement mode**, output Matrix index refers to **measurement order** in circuit:
            [first measured qubit, ..., last measured qubit]

        Args:
            label (str | None): Barrier label to query. If None, returns final output.
            simplify (bool):  If True, simplify before returning.

        Returns:
            sp.Matrix: (2^n, 1) column vector of symbolic probabilities.
        """
        return self.backend.probabilities(label, simplify)
    
    def unitary(self, label_start: str = None, label_end: str = None, simplify: bool = False) -> sp.Matrix:
        """
        Compute the symbolic unitary matrix between two barrier labels.

        Args:
            label_start (str | None): The label of the starting barrier.
                If None, the unitary is computed from the beginning of the circuit.
            label_end (str | None): The label of the ending barrier.
                If None, the unitary is computed up to the end of the circuit.
            simplify (bool): If True, return simplified unitary matrix.

        Returns:
            sympy.Matrix: The composed unitary matrix from `label_start` to `label_end`.

        Raises:
            KeyError: If a provided label does not exist in the circuit.
            ValueError: If any MeasurementChunk is present in the specified range.

        Notes:
            Barrier layers with `label=None` cannot be used as start/end references.

        """
        return self.backend.unitary(label_start, label_end, simplify)
    
    def simplify(self) -> None:
        """
        Simplifies all symbolic states or branches in-place.

        For unitary circuits, this simplifies all statevectors.
        For measurement circuits, this simplifies all measurement branches.

        Caches results to avoid repeated simplification.
        """
        return self.backend.simplify()
    
    def report(self,
        label: Literal["*", None] | str = '*',
        simplify: bool = False,
        output: Literal["auto", "terminal", "notebook"] = 'auto',
        notation: Literal["dirac", "column"] = "column",
    ) -> None:
        """
        Display the symbolic quantum state at a given barrier, final output, or all barrier and final output (default).

        Args:
            label (str | Literal["*", None]): 
                - A specific barrier label to report.
                - "*" to report all barrier states and the final state.
                - None to report only the final statevector.

            simplify (bool):
                Whether to simplify symbolic expressions before displaying them.

            output (str):
                - "auto": detect notebook or terminal automatically
                - "terminal": plain-text output (e.g., for console or logs)
                - "notebook": render using IPython LaTeX display

            notation (str): 
                State representation.
                - "column": sympy Matrix form
                - "dirac": ket-style superposition (e.g. a|000⟩ + b|111⟩)

        """
        self.backend.report(label, simplify, output, notation)


