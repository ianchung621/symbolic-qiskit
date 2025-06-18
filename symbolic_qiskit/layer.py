from dataclasses import dataclass
from typing import List

import sympy as sp
import numpy as np
from qiskit.converters import circuit_to_dag
import qiskit.circuit as qcc
from qiskit import QuantumCircuit

from .standard_gates import gate_to_sympy_matrix

@dataclass
class Operation:
    op: qcc.Instruction
    q_idxs: List[int]

    def __repr__(self) -> str:
        return f"({self.op.name}, q={self.q_idxs})"
    
    @property
    def sym_matrix(self):
        base_matrix = gate_to_sympy_matrix(self.op)
        return base_matrix

@dataclass
class QCLayer:
    operations: List[Operation]


def extract_layer_ops(qc: QuantumCircuit) -> List[QCLayer]:
    """
    Extracts a list of parallelizable QCLayers from a QuantumCircuit.

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit to extract layers from.

    Returns
    -------
    List[QCLayer]
        A list of sequential circuit layers with disjoint operations.
    """
    dag = circuit_to_dag(qc)
    qubit_to_idxs = {q: i for i, q in enumerate(qc.qubits)}
    layers: List[QCLayer] = []

    for layer in dag.layers():
        layer_graph = layer['graph']
        ops: List[Operation] = []
        for node in layer_graph.op_nodes():
            op = node.op
            q_idxs = [qubit_to_idxs[q] for q in node.qargs]
            ops.append(Operation(op=op, q_idxs=q_idxs))
        layers.append(QCLayer(operations=ops))
    
    return layers

def permute_unitary(U_p: sp.Matrix, perm: list[int]) -> sp.Matrix:
    """
    Args:
        U_p (sp.Matrix): Unitary matrix (2^n x 2^n) acting on permuted qubits.
        perm (list[int]): Permutation with len n, maps qubit i to perm[i]

    Returns:
        sp.Matrix: Logical qubit order unitary (P.T * U_p * P).
    """
    n = len(perm)
    dim = 2 ** n

    index_map = np.empty(dim, dtype=int)

    for i in range(dim):
        
        bitstr = format(i, f"0{n}b")
        reordered_bits = [bitstr[perm.index(j)] for j in range(n)] 
        idx = int("".join(reordered_bits), 2)
        index_map[i] = idx
        #print(i, bitstr, reordered_bits, idx)

    U_np = np.array(U_p, dtype=object)
    U_perm_np = U_np[np.ix_(index_map, index_map)]
    return sp.Matrix(U_perm_np)

def construct_layer_matrix(
    qc_layer: QCLayer,
    num_qubits: int
) -> sp.Matrix:
    
    """
    Construct the symbolic unitary matrix for a QCLayer

    Parameters
    ----------
    qc_layer : QCLayer
        A layer of disjoint quantum operations.
    num_qubits : int
        Total number of qubits in the system.

    Returns
    -------
    sp.Matrix
        A 2**num_qubits × 2**num_qubits symbolic unitary matrix.

    """

    sorted_ops = sorted(qc_layer.operations, key=lambda op: -len(op.q_idxs)) # [cx:3,0] [ry:1]
    active_qidxs = [idx for op in sorted_ops for idx in op.q_idxs] # [3,0,1]
    active_gates = [op.sym_matrix for op in sorted_ops] # [cx, ry]

    n_non_active = num_qubits - len(active_qidxs)
    idle_qidxs = [i for i in range(num_qubits) if i not in active_qidxs] 
    permuted_qidxs = active_qidxs + idle_qidxs # active [3,0,1] + idle [2]
    permuted_gates = active_gates + [sp.eye(2)] * n_non_active # [cx, ry, I]
    
    # kron(cx, ry, I) = cx(3,2) ⓧ ry(1) ⓧ I(0), permuted unitary matrix
    U_p = sp.kronecker_product(*permuted_gates)
    # the permute operater that transform [3,2,1,0] to [3,0,1,2]
    perm = [permuted_qidxs.index(i) for i in reversed(range(num_qubits))] # [0,3,2,1]
    return permute_unitary(U_p, perm)