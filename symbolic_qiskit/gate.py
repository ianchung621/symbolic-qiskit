import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import qiskit.circuit as qcc # qiskit circuit class


def get_zero_param_gate_matrix(op_name: str) -> sp.Matrix:
    op_name = op_name.lower()
    # Single Qubit
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
    # Two Qubit
    if op_name in ('cx', 'cnot'):
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])
    elif op_name == 'cz':
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -1]
        ])
    elif op_name == 'swap':
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])
    elif op_name == 'iswap':
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 0, sp.I, 0],
            [0, sp.I, 0, 0],
            [0, 0, 0, 1]
        ])
    # Three Qubit
    if op_name == 'ccx' or op_name == 'toffoli':
        # Flip the target qubit if both control qubits are |1⟩
        # |110⟩ -> |111⟩, |111⟩ -> |110⟩
        mat = sp.eye(8)
        mat[6,6] = 0
        mat[7,7] = 0
        mat[6,7] = 1
        mat[7,6] = 1
        return mat

    elif op_name == 'cswap' or op_name == 'fredkin':
        # Swap qubit 1 and 2 if qubit 0 is |1⟩
        mat = sp.eye(8)
        mat[5,5] = 0  # |101⟩
        mat[6,6] = 0  # |110⟩
        mat[5,6] = 1  # |101⟩ ↔ |110⟩
        mat[6,5] = 1
        return mat
    else:
        raise NotImplementedError(f"Zero-parameter gate '{op_name}' not supported.")

def get_one_param_gate_matrix(op_name: str, theta: float|sp.Symbol) -> sp.Matrix:
    op_name = op_name.lower()
    # Single Qubit
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
    # Two Qubit
    elif op_name == 'rzz':
        return sp.diag(
            sp.exp(-sp.I * theta / 2),
            sp.exp(sp.I * theta / 2),
            sp.exp(sp.I * theta / 2),
            sp.exp(-sp.I * theta / 2)
        )
    else:
        raise NotImplementedError(f"One-parameter gate '{op_name}' not supported.")

def get_three_param_gate_matrix(op_name: str, theta, phi, lam) -> sp.Matrix:
    op_name = op_name.lower()

    if op_name == 'u':
        cos = sp.cos(theta / 2)
        sin = sp.sin(theta / 2)
        e_phi = sp.exp(sp.I * phi)
        e_lam = sp.exp(sp.I * lam)
        e_phi_lam = sp.exp(sp.I * (phi + lam))

        return sp.Matrix([
            [cos, -e_lam * sin],
            [e_phi * sin, e_phi_lam * cos]
        ])
    
    raise ValueError(f"Unsupported 3-parameter gate: {op_name}")

def parse_param(p):
    if isinstance(p, (int, float)):
        return float(p)
    elif isinstance(p, qcc.ParameterExpression):
        expr_str = str(p).replace('[', '_').replace(']', '')
        return parse_expr(expr_str)
    else:
        raise TypeError(f"Unsupported parameter type: {type(p)}")
            
def gate_to_sympy_matrix(gate: qcc.Instruction) -> sp.Matrix:
    op_name = gate.name
    params = gate.params

    if len(params) == 0:
        return get_zero_param_gate_matrix(op_name)
    elif len(params) == 1:
        theta = params[0]
        theta = parse_param(theta)
        return get_one_param_gate_matrix(op_name, theta)
    elif len(params) == 3:
        theta, phi, lam = map(parse_param, params)
        return get_three_param_gate_matrix(op_name, theta, phi, lam)
    else:
        raise NotImplementedError(
            f"Gate '{op_name}' with {len(params)} parameter(s) is not yet supported."
        )