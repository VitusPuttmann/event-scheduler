"""
Invoke the LangGraph application.
"""

from scheduler_graph.agent import graph


if __name__ == "__main__":
    initial_state = {
        "user_input": input("Gib das gewünschte Datum an (im Format JJJJ-MM-TT): ")
    }
    
    graph_result = graph.invoke(initial_state)
    output = graph_result["output"]
    print(output)
