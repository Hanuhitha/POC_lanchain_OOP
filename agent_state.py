from typing import Sequence, TypedDict, Annotated
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, BaseMessage
import operator

class AgentState(TypedDict):
    query: str
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    file_path : str

    

    


     