from sympy.parsing.sympy_parser import parse_expr
import sympy as sp
import qiskit.circuit as qcc

_symbol_cache: dict[str, sp.Symbol] = {}

def get_real_symbol(name: str) -> sp.Symbol:
    """Get or create a real-valued symbol with the given name."""
    if name not in _symbol_cache:
        _symbol_cache[name] = sp.Symbol(name, real=True)
    return _symbol_cache[name]
    
def parse_param(p):
    if isinstance(p, (int, float)):
        return float(p)
    elif isinstance(p, qcc.ParameterExpression):
        expr_str = str(p).replace('[', '_').replace(']', '')
        return parse_real_expr(expr_str)
    else:
        raise TypeError(f"Unsupported parameter type: {type(p)}")

def parse_real_expr(expr_str: str) -> sp.Expr:
    expr = parse_expr(expr_str, evaluate=True)
    symbol_map = {
        sym: get_real_symbol(sym.name)
        for sym in expr.free_symbols
    }
    return expr.subs(symbol_map)

def sp_exp_i(x):
    return sp.exp(sp.I * x)