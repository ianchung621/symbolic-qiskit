from hypothesis import given, strategies, settings

import numpy as np
from qiskit.quantum_info import Statevector

from symbolic_qiskit import CircuitInspector
from tests.utils.random import random_unitary_circuit
from tests.utils.param import generate_parameter_bindings

@given(num_qubits=strategies.integers(min_value=1, max_value=4),
       seed=strategies.integers(min_value=0))
@settings(deadline=None)
def test_unitary_circuit(num_qubits, seed):
    pqc = random_unitary_circuit(
    num_qubits=num_qubits, depth=4, seed=seed)

    qc_binding, sp_binding = generate_parameter_bindings(pqc)
    # qiskit
    arr_qiskit = Statevector(pqc.assign_parameters(qc_binding)).data
    # symbolic-qiskit
    final_state = CircuitInspector(pqc).statevector()
    final_state_data = final_state.subs(sp_binding).evalf()
    arr_symb = np.array(final_state_data, dtype=np.complex128).ravel()
    assert np.allclose(arr_qiskit, arr_symb)


