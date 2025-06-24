from qiskit.circuit.random import random_circuit
from qiskit.circuit import ParameterVector
from qiskit import QuantumCircuit

def random_unitary_circuit(num_qubits, depth, max_operands=3, seed=None):
    random_qc = random_circuit(
        num_qubits=num_qubits, depth=depth, max_operands=max_operands, seed=seed)
    random_pqc = QuantumCircuit(random_qc.num_qubits, random_qc.num_qubits)
    
    num_params = sum(len(instruction.operation.params)
                     for instruction in random_qc)
    x = ParameterVector(name='x', length=num_params)
    i = 0
    for instruction in random_qc:
        op = instruction.operation.to_mutable()
        n = len(op.params)
        op.params = x[i:i+n]
        i += n
        random_pqc.append(op, qargs=instruction.qubits)
    
    return random_pqc