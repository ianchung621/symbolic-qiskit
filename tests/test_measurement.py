from hypothesis import given, strategies, settings, Verbosity

import numpy as np
from qiskit.quantum_info import Statevector

from symbolic_qiskit import CircuitInspector
from tests.utils.random import random_unitary_circuit
from tests.utils.param import generate_parameter_bindings, deep_evalf

@given(num_qubits=strategies.integers(min_value=1, max_value=4),
       seed=strategies.integers(min_value=0, max_value=1000))
@settings(deadline=None, max_examples=20)
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
    try:
        probs_data = probs.subs(sp_binding).evalf()
        arr_symb = np.array(probs_data, dtype=np.complex128).ravel()
    except:
        probs_data = deep_evalf(probs.subs(sp_binding)) # for extreme long expression 
        arr_symb = np.array(probs_data, dtype=np.complex128).ravel()

    assert np.allclose(arr_qiskit, arr_symb)