"""
Visualize the complete LangGraph graph.
"""

import sys
from pathlib import Path

from IPython.display import Image, display
from langchain_core.runnables.graph import MermaidDrawMethod


sys.path.append(str(Path("..").resolve()))
from scheduler_graph.agent import graph


def show_graph() -> None:
    display(
        Image(
            graph.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )
        )
    )
