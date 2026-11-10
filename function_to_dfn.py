from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import to_dnf

def function_to_dfn(function: str):
    _, term = function.split(':')

    import re
    tokens = re.findall(r'[A-Za-z][A-Za-z0-9_]*', term)
    tokens = list(dict.fromkeys(tokens))

    sympy_symbols = {t: symbols(t) for t in tokens}

    term = term.replace('!', '~')

    sympy_term = parse_expr(term, local_dict=sympy_symbols)
    sympy_term = to_dnf(sympy_term, simplify=True)

    return str(sympy_term).replace('~', '!')