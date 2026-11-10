from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import to_dnf

def function_to_dfn(function: str):
    import re
    tokens = re.findall(r'[A-Za-z][A-Za-z0-9_]*', function)
    tokens = list(dict.fromkeys(tokens))

    sympy_symbols = {t: symbols(t) for t in tokens}

    function = function.replace('!', '~')

    sympy_function = parse_expr(function, local_dict=sympy_symbols)
    sympy_function = to_dnf(sympy_function, simplify=True)

    return str(sympy_function).replace('~', '!')

def compare_functions(f1: str, f2: str) -> bool:
    dfn1 = function_to_dfn(f1)
    dfn2 = function_to_dfn(f2)

    return dfn1 == dfn2