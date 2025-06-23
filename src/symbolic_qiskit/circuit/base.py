import sympy as sp

from dataclasses import dataclass
from qiskit.circuit import ParameterExpression
from ..layer import QCLayer, StandardGateLayer, MeasurementLayer, BarrierLayer, MeasurementBranch
from ..layer import construct_layer_matrix, apply_measurement_layer

class Chunk:
    layers: list[QCLayer]

@dataclass
class ChunkedCircuit:
    chunks: list[Chunk | BarrierLayer]
    global_phase: float | ParameterExpression

@dataclass
class StandardGateChunk(Chunk):
    layers: list[StandardGateLayer]

    def get_matrix(self, num_qubits: int):
        U = sp.eye(2**num_qubits)
        for layer in self.layers:
            U_layer = construct_layer_matrix(layer, num_qubits)
            U = U_layer * U
        return U

@dataclass
class MeasurementChunk(Chunk):
    layers: list[MeasurementLayer]

    def apply_measurement(self, current_branches: list[MeasurementBranch]):
        for layer in self.layers:
            current_branches = apply_measurement_layer(current_branches, layer)
        return current_branches