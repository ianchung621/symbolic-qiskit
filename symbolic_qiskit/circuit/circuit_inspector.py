from typing import Literal

import sympy as sp
from qiskit import QuantumCircuit

from .build import circuit_to_chunks
from .base import MeasurementChunk, MeasurementBranch, BarrierLayer
from .measuremet_circuit import MeasurementCircuitBackend
from .unitary_circuit import UnitaryCircuitBackend

class CircuitInspector:
    def __init__(self, qc: QuantumCircuit):
        chunks = circuit_to_chunks(qc)
        #self.chunks = chunks
        #self.num_qubits = qc.num_qubits
        self.has_measurement = any(isinstance(c, MeasurementChunk) for c in chunks)
        self.mode: Literal["unitary", "measurement"] = (
            "measurement" if self.has_measurement else "unitary"
        )

        if self.mode == "unitary":
            self.backend = UnitaryCircuitBackend(chunks, qc.num_qubits)
        else:
            self.backend = MeasurementCircuitBackend(chunks, qc.num_qubits)

    def statevector(self, label: str) -> sp.Matrix:
        if self.mode != "unitary":
            raise RuntimeError("Cannot query `statevector()` on a circuit with measurement — use `branches()` instead.")
        return self.backend.statevector(label)

    def unitary(self, label_start: str, label_end: str = None) -> sp.Matrix:
        return self.backend.unitary(label_start, label_end)

    def branches(self, label: str) -> list[MeasurementBranch]:
        if self.mode != "measurement":
            raise RuntimeError("Circuit has no measurements — use `statevector()` instead.")
        return self.backend.branches(label)


