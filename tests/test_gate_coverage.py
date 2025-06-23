from qiskit.circuit.library import get_standard_gate_name_mapping
from symbolic_qiskit.gate.standard_gates import SUPPORTED_GATES

def test_gate_coverage():
    qiskit_gates = set(get_standard_gate_name_mapping().keys())
    expected_qiskit_gates = qiskit_gates - {'delay','reset','measure','global_phase'}
    missing = expected_qiskit_gates - SUPPORTED_GATES
    assert not missing, f"Missing symbolic implementations for: {sorted(missing)}"