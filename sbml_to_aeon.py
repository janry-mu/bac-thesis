from biodivine_aeon import BooleanNetwork

def sbml_to_aeon(sbml_f: str, aeon_f: str):
    bn = BooleanNetwork.from_file(sbml_f, repair_graph=True)

    with open(aeon_f, "w", encoding="utf-8") as f:
        f.write(bn.to_aeon())