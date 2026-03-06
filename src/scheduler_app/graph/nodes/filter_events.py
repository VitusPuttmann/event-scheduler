"""
Node for filtering events.
"""

from typing import List, Optional

from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt

from scheduler_app.models.event import Event
from scheduler_app.graph.state import AgentState


def filter_events(
        state: AgentState, config: Optional[RunnableConfig] = None
    ) -> dict[str, List[Event]]:
    """
    Filter list of events based on user input on preferred event type.
    """

    type_map = {
        "Klassik": ("1", "Klassik"),
        "Jazz, Blues, Funk": ("2", "Jazz, Blues, Funk"),
        "Rock, Indie, Metal": ("3", "Rock, Indie, Metal"),
        "HipHop, RnB, Soul": ("4", "HipHop, RnB, Soul"),
        "Elektro, Techno, House": ("5", "Elektro, Techno, House"),
        "Pop, Schlager": ("6", "Pop, Schlager")
    }
    type_map_rev = {num: t for t, (num, _) in type_map.items()}

    event_types = [
        e.event_type for e in state.events_list if e.event_type is not None
    ]

    seen = set()
    event_types_unique = [
        t for t in event_types if not (t in seen or seen.add(t))
    ]

    if not event_types_unique:
        events_filtered = []
    else:
        event_types_unique_numbered = [
            f"{type_map[e][0]} {type_map[e][1]}" for e in event_types_unique
        ]

        user_choice = interrupt({
            "question": "Welches Musikgenre möchtest Du hören? Gib die dazugehörige Nummer an.",
            "data": event_types_unique_numbered
        })
        user_choice = str(user_choice).strip()
        
        event_type_selected = type_map_rev.get(user_choice)

        if event_type_selected:
            matching_events = [
                e for e in state.events_list if
                    e.event_type == event_type_selected
            ]
            events_filtered = matching_events[:1]
        else:
            events_filtered = []
    
    # Update state
    updated_state = {
        "events_list_filtered": events_filtered
    }
    return updated_state
