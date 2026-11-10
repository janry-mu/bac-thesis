from biodivine_aeon import BooleanNetwork
import re

def sbml_to_aeon(sbml_f: str, aeon_f: str):
    bn = BooleanNetwork.from_file(sbml_f, repair_graph=True)

    with open(aeon_f, "w", encoding="utf-8") as f:
        f.write(bn.to_aeon())


def sort_file(file: str):
    with open(file, encoding="utf-8") as f:
        lines = f.read().splitlines()

    lines.sort(key=str.lower)

    with open(file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def remove_notes(file: str, note_marker="#") -> int:
    with open(file, encoding="utf-8") as f:
        lines = f.read().splitlines()

    removed_counter = 0
    with open(file, "w", encoding="utf-8") as f:
        for line in lines:
            if len(line) == 0 or (len(line) != 0 and line[0] != note_marker):
                f.write(line + "\n")
            else:
                removed_counter += 1
    return removed_counter

def find_PSFs(file: str,
              function_symbol='$',
              function_pattern=r'cat_[^(]*\(([^)]*)\)') -> dict[str,str]:
    result = {}
    
    with open(file, encoding="utf-8") as f:
        lines = f.read().splitlines()

    for line in lines:
        if line != "" and line[0] == function_symbol and re.search(function_pattern, line):
            node_name, term = line.split(':')
            result[node_name] = term

    return result