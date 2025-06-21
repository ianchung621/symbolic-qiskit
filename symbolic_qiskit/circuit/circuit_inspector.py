from typing import Literal

import sympy as sp
from qiskit import QuantumCircuit

from .build import circuit_to_chunks
from .base import MeasurementChunk, MeasurementBranch, BarrierLayer
from .measurement_circuit import MeasurementCircuitBackend
from .unitary_circuit import UnitaryCircuitBackend

class CircuitInspector:
    def __init__(self, qc: QuantumCircuit):
        chunks = circuit_to_chunks(qc)
        self.has_measurement = any(isinstance(c, MeasurementChunk) for c in chunks)
        self.mode: Literal["unitary", "measurement"] = (
            "measurement" if self.has_measurement else "unitary"
        )

        if self.mode == "unitary":
            self.backend = UnitaryCircuitBackend(chunks, qc.num_qubits)
        else:
            self.backend = MeasurementCircuitBackend(chunks, qc.num_qubits)

    def statevector(self, label: str|None = None) -> sp.Matrix:
        """
        Returns the symbolic statevector at the given barrier label.

        Args:
            label (str | None): Barrier label to query.
                If None, return the final statevector of the circuit

        Returns:
            sympy.Matrix: Statevector at the specified barrier.
        """
        if self.mode != "unitary":
            raise RuntimeError("Cannot query `statevector()` on a circuit with measurement — use `branches()` instead.")
        return self.backend.statevector(label)

    def branches(self, label: str|None = None) -> list[MeasurementBranch]:
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

        Returns:
            list[MeasurementBranch]: branches at the specified barrier.
        """
        if self.mode != "measurement":
            raise RuntimeError("Circuit has no measurements — use `statevector()` instead.")
        return self.backend.branches(label)
    
    def unitary(self, label_start: str = None, label_end: str = None) -> sp.Matrix:
        """
        Compute the symbolic unitary matrix between two barrier labels.

        Args:
            label_start (str | None): The label of the starting barrier.
                If None, the unitary is computed from the beginning of the circuit.
            label_end (str | None): The label of the ending barrier.
                If None, the unitary is computed up to the end of the circuit.

        Returns:
            sympy.Matrix: The composed unitary matrix from `label_start` to `label_end`.

        Raises:
            KeyError: If a provided label does not exist in the circuit.
            ValueError: If any MeasurementChunk is present in the specified range.

        Notes:
            Barrier layers with `label=None` cannot be used as start/end references.

        """
        return self.backend.unitary(label_start, label_end)


