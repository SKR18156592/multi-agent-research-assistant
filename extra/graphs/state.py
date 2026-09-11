from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_core.messages import AnyMessage


class ResearchGraphState(TypedDict):
    topic:str # Research topic
    max_analysts:int # Number of analysts
    human_analyst_feedback:str # Human feedback
    analysts:list[Analyst] # Analyst asking questions
    sections:Annotated[list[str],add] # Send() API key
    introduction:str # Introduction for the final report
    content:str # Content for the final report
    conclusion:str # Conclusion for the final report
    final_report:str # Final report
    

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