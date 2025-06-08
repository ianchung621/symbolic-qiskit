import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from qiskit import QuantumCircuit
import qiskit.circuit as qcc # qiskit circuit class

def get_zero_param_gate_matrix(op_name: str) -> sp.Matrix:
    op_name = op_name.lower()
    if op_name == 'i':
        return sp.eye(2)
    elif op_name == 'h':
        return 1 / sp.sqrt(2) * sp.Matrix([
            [1, 1],
            [1, -1]
        ])
    elif op_name == 'x':
        return sp.Matrix([
            [0, 1],
            [1, 0]
        ])
    elif op_name == 'y':
        return sp.Matrix([
            [0, -sp.I],
            [sp.I, 0]
        ])
    elif op_name == 'z':
        return sp.Matrix([
            [1, 0],
            [0, -1]
        ])
    elif op_name == 's':
        return sp.Matrix([
            [1, 0],
            [0, sp.I]
        ])
    elif op_name == 'sdg':
        return sp.Matrix([
            [1, 0],
            [0, -sp.I]
        ])
    elif op_name == 't':
        return sp.Matrix([
            [1, 0],
            [0, sp.exp(sp.I * sp.pi / 4)]
        ])
    elif op_name == 'tdg':
        return sp.Matrix([
            [1, 0],
            [0, sp.exp(-sp.I * sp.pi / 4)]
        ])
    else:
        raise NotImplementedError(f"Zero-parameter gate '{op_name}' not supported.")

def get_one_param_gate_matrix(op_name: str, theta: float|sp.Symbol) -> sp.Matrix:
    op_name = op_name.lower()
    if op_name == 'rx':
        return sp.Matrix([
            [sp.cos(theta / 2), -sp.I * sp.sin(theta / 2)],
            [-sp.I * sp.sin(theta / 2), sp.cos(theta / 2)]
        ])
    elif op_name == 'ry':
        return sp.Matrix([
            [sp.cos(theta / 2), -sp.sin(theta / 2)],
            [sp.sin(theta / 2),  sp.cos(theta / 2)]
        ])
    elif op_name == 'rz':
        return sp.Matrix([
            [sp.exp(-sp.I * theta / 2), 0],
            [0, sp.exp(sp.I * theta / 2)]
        ])
    elif op_name == 'u1':
        return sp.Matrix([
            [1, 0],
            [0, sp.exp(sp.I * theta)]
        ])
    else:
        raise NotImplementedError(f"One-parameter gate '{op_name}' not supported.")

def gate_to_sympy_matrix(gate: qcc.Instruction) -> sp.Matrix:
    op_name = gate.name
    params = gate.params

    if len(params) == 0:
        return get_zero_param_gate_matrix(op_name)
    elif len(params) == 1:
        theta = params[0]
        if isinstance(theta, (int, float)):
            theta = float(theta)
        elif isinstance(theta, qcc.ParameterExpression):
            expr_str = str(theta).replace('[', '_').replace(']', '')
            theta = parse_expr(expr_str)
        else:
            raise TypeError(f"Unsupported parameter type: {type(theta)}")

        return get_one_param_gate_matrix(op_name, theta)
    else:
        raise NotImplementedError(
            f"Gate '{op_name}' with {len(params)} parameter(s) is not yet supported."
        )

def single_qubit_circuit_to_sympy(qc: QuantumCircuit) -> sp.Matrix:
    """
    Convert a single-qubit QuantumCircuit into its symbolic unitary matrix.
    """
    U: sp.Matrix = sp.eye(2)

    for instruction in qc.data:
        op: qcc.Instruction = instruction.operation 
        gate_matrix = gate_to_sympy_matrix(op)
        U = gate_matrix * U

    return U