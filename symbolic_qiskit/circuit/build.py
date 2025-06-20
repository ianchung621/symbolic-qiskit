from qiskit import QuantumCircuit, transpile

from .base import QCLayer, Chunk, StandardGateChunk, MeasurementChunk
from ..layer import StandardGateLayer, BarrierLayer, MeasurementLayer, circuit_to_layers
from ..gate import BASIS_GATES

def circuit_to_chunks(qc: QuantumCircuit) -> list[Chunk | BarrierLayer]:
    transpiled_qc = transpile(qc, basis_gates=BASIS_GATES, optimization_level=1)
    layers = circuit_to_layers(transpiled_qc)
    return layers_to_chunks(layers)

def layers_to_chunks(layers: list[QCLayer]) -> list[Chunk | BarrierLayer]:
    result = []
    current_chunk: list[QCLayer] = []

    def flush_chunk():
        if not current_chunk:
            return
        if all(isinstance(l, StandardGateLayer) for l in current_chunk):
            result.append(StandardGateChunk(current_chunk.copy()))
        elif all(isinstance(l, MeasurementLayer) for l in current_chunk):
            result.append(MeasurementChunk(current_chunk.copy()))
        else:
            raise ValueError("Mixed layer types within chunk.")
        current_chunk.clear()

    for layer in layers:
        if isinstance(layer, BarrierLayer):
            flush_chunk()
            result.append(layer)
        else:
            if current_chunk and type(layer) != type(current_chunk[-1]):
                flush_chunk()
            current_chunk.append(layer)

    flush_chunk()
    return result
