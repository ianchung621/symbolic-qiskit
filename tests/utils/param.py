import numpy as np
import sympy as sp
from qiskit import QuantumCircuit

def generate_parameter_bindings(pqc: QuantumCircuit):
    """return qc_binding, sp_binding(qc.param:val, sp.symbol:val) """
    params = pqc.parameters
    params_sp = [sp.Symbol(str(p).replace('[','_').replace(']',''), real=True) for p in params]
    values = np.random.rand(len(params)) * 2*np.pi
    return dict(zip(params, values)), dict(zip(params_sp, values))

def deep_evalf(expr, n=15):
    if isinstance(expr, sp.Matrix):
        return expr.applyfunc(lambda x: deep_evalf(x, n))
    elif isinstance(expr, sp.Basic):
        return expr.xreplace({
            arg: deep_evalf(arg, n)
            for arg in expr.args
        }).evalf(n)
    else:
        return expr  # numeric