from typing import Literal, Tuple

import sympy as sp
import numpy as np

def permute_qubit_unitary(U_p: sp.Matrix, perm: list[int]) -> sp.Matrix:
    """
    Args:
        U (sp.Matrix): matrix on qubits U (2^n x 2^n)
        perm (list[int]): permutation list (n), maps qubit i to perm[i]

    Returns:
        U_p (sp.Matrix): matrix on permuted qubits, U_p = P.T * U * P
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

def state_vector_projection(state_vector: sp.Matrix, q_idx: int, collapsed_state: Literal[0,1]) -> Tuple[sp.Expr,sp.Matrix]:
    """
    Args:
        state_vector (sp.Matrix): Input state vector of size 2^n (column vector), with shape (2^n, 1)
        q_idx (int): Index of the measured qubit (little-endian)
        collapsed_state (Literal[0, 1]): Measurement outcome (0 or 1).

    Returns:
        Tuple[sp.Expr,sp.Matrix]: Probability of measurement outcome, normalized projected state (or zero vector if probability is zero)
        
    """
    dim: int = state_vector.shape[0]
    n_qubits = dim.bit_length() - 1

    if not (0 <= q_idx < n_qubits):
        raise ValueError(f"Invalid qubit index: {q_idx}. Expected range 0 to {n_qubits - 1}.")
    
    indices = []
    for i in range(dim):
        bitstr = format(i, f"0{n_qubits}b")
        if int(bitstr[n_qubits - 1 - q_idx]) == collapsed_state:
            indices.append(i)

    projected = sp.Matrix([
        state_vector[i] if i in indices else 0
        for i in range(dim)
    ])
    prob = (projected.H * projected)[0]
    normalized = projected if prob == 0 else projected / projected.norm()
    
    return prob, normalized