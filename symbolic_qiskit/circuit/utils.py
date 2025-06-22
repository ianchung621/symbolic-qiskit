from typing import Literal

import sympy as sp

def _use_notebook(output: Literal["auto", "terminal", "notebook"]) -> bool:
    if output == "notebook":
        return True
    if output == "terminal":
        return False
    if output == "auto":
        try:
            from IPython import get_ipython
            shell = get_ipython()
            return shell is not None and shell.has_trait("kernel")
        except Exception:
            return False
    raise ValueError(f"Invalid output: {output}")

def _display_expr(
    expr: sp.Expr | sp.Matrix,
    use_notebook: bool,
    use_dirac: bool,
    num_qubits: int | None = None,
) -> None:
    if isinstance(expr, sp.Expr):
        latex_str = sp.latex(expr)

    elif isinstance(expr, sp.Matrix) and use_dirac:
        terms = []
        for i, amp in enumerate(expr):
            if amp != 0:
                ket = format(i, f"0{num_qubits}b")
                amp_latex = sp.latex(amp)
                terms.append(f"{amp_latex}\\left|{ket}\\right\\rangle")

        latex_str = "0" if not terms else " + ".join(terms)

    elif isinstance(expr, sp.Matrix):
        latex_str = sp.latex(expr)

    if use_notebook:
        from IPython.display import display_latex, Math
        display_latex(Math(latex_str))
    else:
        print(latex_str)


