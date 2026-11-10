from dotenv import load_dotenv
from google import genai

TASK = """\
    Your goal is to identify a function of an edge in a boolean network that represents a biological pathway.
    You will recieve the name of a node in the boolean network and its partial identified update function.
    You have to decide the complete version of it. The undecided part of the function is noted like this:
    cat_name_of_the_node_number(atr1, atr2, ...). You have to decide how the atributes fit into the rest of the function.
    If you cannot determine the complete function, answer: \"Function could not be determined.\".
    If you determine the complete function, your answer should only be the function and no other text.
    Determined function should only use symbols from the function I gave you and "&" as and, "|" as or, "!" as negation. 
    """

def gemini(node_name: str, function: str, task=TASK):
    load_dotenv()
    client = genai.Client()

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=f"""\
                    Context: {task}\n
                    Node: {node_name}\n
                    Function: {function}
                """
        )
        
        if interaction.output_text is None:
            return None

        return interaction.output_text

    except Exception as e:
        print(f"Gemini chyba: {e}")
        return None