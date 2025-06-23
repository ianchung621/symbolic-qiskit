from sympy.parsing.sympy_parser import parse_expr
import sympy as sp
import qiskit.circuit as qcc

def parse_param(p):
    if isinstance(p, (int, float)):
        return float(p)
    elif isinstance(p, qcc.ParameterExpression):
        expr_str = str(p).replace('[', '_').replace(']', '')
        return parse_real_expr(expr_str)
    else:
        raise TypeError(f"Unsupported parameter type: {type(p)}")

def parse_real_expr(expr_str: str) -> sp.Expr:
    
    def real_symbol(name):
        return sp.Symbol(name, real=True)

    return parse_expr(expr_str, local_dict={}, global_dict={"Symbol": real_symbol})

def sp_exp_i(x):
    return sp.exp(sp.I * x)