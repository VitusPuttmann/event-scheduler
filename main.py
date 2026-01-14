"""
Invoke the LangGraph application.
"""

from dotenv import load_dotenv

from scheduler_graph.agent import graph


load_dotenv()


if __name__ == "__main__":
    initial_state = {
        "user_input_date": input("Gib das gewünschte Datum an (im Format JJJJ-MM-TT): "),
        "user_input_type": input("Gib die gewünschte Veranstaltungsart an (z.B. Konzert oder Musical): ")
    }
    
    graph_result = graph.invoke(initial_state)
    output = graph_result["output"]
    print(output)
