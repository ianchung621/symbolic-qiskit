import sympy as sp

from .base import StandardGateLayer
from .utils import permute_qubit_unitary

def construct_layer_matrix(
    layer: StandardGateLayer,
    num_qubits: int
) -> sp.Matrix:
    
    """
    Construct the symbolic unitary matrix for a StandardGateLayer

    Parameters
    ----------
    layer :  StandardGateLayer
    num_qubits : int

    Returns
    -------
    U : sp.Matrix
        symbolic unitary matrix (2^n x 2^n)

    """

    sorted_ops = sorted(layer.ops, key=lambda op: -len(op.q_idxs)) # [cx:3,0] [ry:1] num_qubit: 4
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
    return permute_qubit_unitary(U_p, perm)