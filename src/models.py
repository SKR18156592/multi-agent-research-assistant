from operator import add
from typing import Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

class Analyst(BaseModel):
    affiliation: str = Field(description="Primary affiliation of the analyst")
    name: str = Field(description="Name of the analyst")
    role: str = Field(description="Role of the analyst in the context of the topic")
    description: str = Field(description="Description of the analyst's focus, concern and motives")

    @property
    def persona(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Role: {self.role}\n"
            f"Affiliation: {self.affiliation}\n"
            f"Description: {self.description}\n"
        )

class Perspectives(BaseModel):
    analysts: list[Analyst] = Field(
        description="Comprehensive list of analysts with their roles and affiliations."
    )

class GenerateAnalystState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str | None
    analysts: list[Analyst]

class SearchQuery(BaseModel):
    search_query: str = Field(
        None,
        description="Search query for retrieval"
    )

class InterviewState(MessagesState):
    max_num_turns: int
    context: Annotated[list[str], add]
    analyst: Analyst
    interview: str
    sections: str

class ResearchGraphState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str | None
    analysts: list[Analyst]
    sections: Annotated[list[str], add]
    introduction: str
    content: str
    conclusion: str
    final_report: str