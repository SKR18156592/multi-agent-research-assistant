from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_core.messages import AnyMessage

class Analyst(TypedDict):
    name: str
    role: str
    affiliation: str
    description: str

class InterviewState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    analyst: Analyst
    interview_summary: Optional[str]

class ResearchState(TypedDict):
    topic: str
    max_analysts: int
    analysts: List[Analyst]
    sections: Annotated[List[str], operator.add]
    final_report: Optional[str]