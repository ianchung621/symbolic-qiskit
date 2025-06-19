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