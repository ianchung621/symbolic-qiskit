import qiskit.circuit as qcc
from qiskit import QuantumCircuit

from .base import StandardGate, Barrier, Measurement, QCLayer, StandardGateLayer, BarrierLayer, MeasurementLayer
from ..gate import SUPPORTED_GATES

def circuit_to_layers(qc: QuantumCircuit) -> list[QCLayer]:
    layers = []
    current_ops = []
    current_type = None
    active_q = set()
    active_c = set()

    qubit_to_idx = {q: i for i, q in enumerate(qc.qubits)}
    clbit_to_idx = {c: i for i, c in enumerate(qc.clbits)}

    def flush():
        nonlocal current_ops, current_type, active_q, active_c
        if not current_ops:
            return
        if current_type == 'gate':
            layers.append(StandardGateLayer(current_ops))
        elif current_type == 'measure':
            layers.append(MeasurementLayer(current_ops))
        elif current_type == 'barrier':
            layers.append(BarrierLayer(current_ops))
        current_ops = []
        active_q.clear()
        active_c.clear()
        current_type = None

    for inst in qc.data:
        op: qcc.Instruction = inst.operation
        q_idxs = [qubit_to_idx[q] for q in inst.qubits]
        c_idxs = [clbit_to_idx[c] for c in inst.clbits]
        q_set = set(q_idxs)
        c_set = set(c_idxs)

        if op.name == "barrier":
            if current_type not in (None, 'barrier'):
                flush()
            current_type = 'barrier'
            current_ops.append(Barrier(op, q_idxs, op.label))
            continue

        elif op.name == "measure":
            if current_type != 'measure' or (q_set & active_q) or (c_set & active_c):
                flush()
            current_type = 'measure'
            current_ops.append(Measurement(op, q_idxs, c_idxs))
            active_q.update(q_set)
            active_c.update(c_set)

        elif op.name in SUPPORTED_GATES:
            if current_type != 'gate' or (q_set & active_q):
                flush()
            current_type = 'gate'
            current_ops.append(StandardGate(op, q_idxs))
            active_q.update(q_set)
        elif op.name == 'delay':
            continue
        else:
            raise ValueError(f"Unsupported operation '{op.name}' in circuit, supported operations: {SUPPORTED_GATES}")

    flush()
    return layers
