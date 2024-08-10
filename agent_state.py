from typing import Sequence, TypedDict, Annotated
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, BaseMessage
import operator


class AgentState(TypedDict):
    """AgentState to share data between nodes in langraph."""

    query: str
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    error: str
    code_file_path: str
    summary_file_path: str
    audio_file_path: str

