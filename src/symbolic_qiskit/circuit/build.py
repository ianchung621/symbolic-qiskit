from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Instruction

from .base import QCLayer, Chunk, ChunkedCircuit, StandardGateChunk, MeasurementChunk, StandardGateLayer, BarrierLayer, MeasurementLayer
from ..layer import circuit_to_layers
from ..gate import SUPPORTED_GATES

def circuit_to_chunks(qc: QuantumCircuit) -> ChunkedCircuit:
    supported_gates = SUPPORTED_GATES | {'delay','measure','barrier'}
    unsupported_gates = {'reset','global_phase'}
    decomposed_qc = decompose_to_standard_gates(qc, supported_gates, unsupported_gates)
    layers = circuit_to_layers(decomposed_qc)
    return ChunkedCircuit(layers_to_chunks(layers), qc.global_phase)

def decompose_to_standard_gates(
    quantum_circuit: QuantumCircuit,
    supported_gates: set[str],
    unsupported_gates: set[str]
) -> QuantumCircuit:
    
    def needs_decompose(op: Instruction):
        return (
            op.name not in supported_gates
            and hasattr(op, 'definition')
            and op.definition is not None
        )

    qc = quantum_circuit

    while True:
        decomposed = False
        new_qc = QuantumCircuit(*qc.qregs, *qc.cregs)

        for ins in qc.data:
            op: Instruction = ins.operation
            qargs, cargs = ins.qubits, ins.clbits

            if op.name in unsupported_gates:
                raise ValueError(f"Unsupported gate '{op.name}' encountered.")

            if needs_decompose(op):
                sub_qc: QuantumCircuit | None = op.definition.copy()
                sub_qc = sub_qc.assign_parameters(op.params)
                sub_qc = sub_qc.decompose()

                for sub_ins in sub_qc.data:
                    new_qc.append(
                        sub_ins.operation,
                        [qargs[i] for i in range(len(sub_ins.qubits))],
                        cargs
                    )
                decomposed = True
            else:
                new_qc.append(op, qargs, cargs)

        qc = new_qc
        if not decomposed:
            break

    return qc

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
