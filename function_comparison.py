from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import to_dnf
import subprocess, re, os
from edit_file import sbml_to_aeon
from llm_function_finder import gemini

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


def find_PSFs(psf_file: str,
              ref_file: str,
              function_symbol='$',
              function_pattern=r'cat_[^(]*\(([^)]*)\)') -> dict[str, tuple[str,str]]:
    result = {}
    
    with open(psf_file, encoding="utf-8") as f:
        psf_lines = f.read().splitlines()
    with open(ref_file, encoding="utf-8") as f:
        ref_lines = f.read().splitlines()

    for line in psf_lines:
        if line != "" and line[0] == function_symbol and re.search(function_pattern, line):
            node_name, function = line.split(':')
            ref_function = ""

            for ref in ref_lines:
                if ref.startswith(node_name):
                    _, ref_function = ref.split(':')

            result[node_name] = (function, ref_function)

    return result


def run_casq(map_path: str, venv_path: str, output_path: str, option=""):
    sbp = [venv_path, map_path, output_path] if option == "" else [venv_path, option, map_path, output_path]
    subprocess.run(
        sbp
    )


def compare_casqs(sbgn_path: str,
                  cd_path: str,
                  casq_output_path: str,
                  fcasq_output_path: str,
                  casq_venv_path="casq\\Scripts\\casq.exe",
                  fcasq_venv_path="fcasq\\Scripts\\casq.exe"):
    run_casq(sbgn_path, casq_venv_path, casq_output_path + ".sbml")
    run_casq(cd_path, fcasq_venv_path, fcasq_output_path + ".aeon", "-a")

    sbml_to_aeon(casq_output_path + ".sbml", casq_output_path + ".aeon")
    os.remove(casq_output_path + ".sbml")

    psfs = find_PSFs(fcasq_output_path + ".aeon", casq_output_path + ".aeon")

    for node_name, functions in psfs.items():
        function, ref = functions
        llm_decided_function = gemini(node_name, function)
        if llm_decided_function is not None and not compare_functions(llm_decided_function, ref):
            print(f"Node: {node_name}\nFunction: {ref}\nLLM result: {llm_decided_function}\n---")

compare_casqs("test\\network.sbgn", "test\\network.xml", "casq_comparison\\casq", "casq_comparison\\fcasq")