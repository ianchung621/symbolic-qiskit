from tests.utils.random import random_unitary_circuit
from symbolic_qiskit import CircuitInspector


def test_imports_only():
    assert callable(random_unitary_circuit)
    assert CircuitInspector is not None
