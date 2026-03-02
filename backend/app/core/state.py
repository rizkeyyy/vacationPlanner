from enum import Enum
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class PlannerStatus(str, Enum):
    IDLE = "IDLE"
    EXTRACTING = "EXTRACTING"
    RETRIEVING_PREF = "RETRIEVING_PREF"
    VALIDATING = "VALIDATING"
    SEARCHING = "SEARCHING"
    EVALUATING = "EVALUATING"
    AWAITING_CONFIRMATION = "AWAITING_CONFIRMATION"
    BOOKING = "BOOKING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

#LANGGRAPH
class AgentState(TypedDict):
    
    messages: Annotated[list, add_messages]
    