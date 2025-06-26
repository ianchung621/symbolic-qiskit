from hypothesis import given, strategies, settings, Verbosity

import numpy as np
import sympy as sp
from qiskit.quantum_info import Statevector

from symbolic_qiskit import CircuitInspector
from tests.utils.random import random_unitary_circuit
from tests.utils.param import generate_parameter_bindings, deep_evalf

@given(num_qubits=strategies.integers(min_value=1, max_value=3),
       seed=strategies.integers(min_value=0))
@settings(deadline=None, max_examples=10)
def test_measurement_circuit(num_qubits, seed):
    pqc = random_unitary_circuit(
    num_qubits=num_qubits, depth=4, seed=seed)

    qc_binding, sp_binding = generate_parameter_bindings(pqc)
    # qiskit
    arr_qiskit = Statevector(pqc.assign_parameters(qc_binding)).probabilities()
    # symbolic-qiskit
    meas_idxs = list(reversed(range(num_qubits))) # measure from bit_n to bit_1
    pqc.measure(meas_idxs, meas_idxs)
    probs = CircuitInspector(pqc).probabilities()
    arr_symb = _evaluate_symbolic_probabilities(probs, sp_binding)

    assert np.allclose(arr_qiskit, arr_symb)


def _evaluate_symbolic_probabilities(expr: sp.Matrix, bindings):
    try:
        probs_data = expr.subs(bindings).evalf()
        arr = np.array(probs_data, dtype=np.complex128).ravel()
    except:
        probs_data = deep_evalf(expr.subs(bindings)) # expr too long that .evalf fail to handle
        arr = np.array(probs_data, dtype=np.complex128).ravel() 

    if np.isnan(arr).any():
        simplified_expr = expr.applyfunc(sp.simplify) # unlucky case with nan value, probably from 0 division
        try:
            probs_data = simplified_expr.subs(bindings).evalf()
            arr = np.array(probs_data, dtype=np.complex128).ravel()
        except:
            probs_data = deep_evalf(simplified_expr.subs(bindings))
            arr = np.array(probs_data, dtype=np.complex128).ravel()
    
    return arr