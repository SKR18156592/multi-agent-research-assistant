from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from prompts.analyst_prompts import ANALYST_PERSONA_GENERATOR_PROMPT

class AnalystPersona(BaseModel):
    name: str = Field(description="Name of the analyst")
    role: str = Field(description="Their professional role")
    affiliation: str = Field(description="Organization or domain area")
    description: str = Field(description="Focus area and angle of inquiry")

class AnalystList(BaseModel):
    analysts: List[AnalystPersona]

def create_analysts(topic: str, max_analysts: int, model_name: str = "gpt-4o"):
    llm = ChatOpenAI(model=model_name, temperature=0.7)
    structured_llm = llm.with_structured_output(AnalystList)
    prompt = ChatPromptTemplate.from_template(ANALYST_PERSONA_GENERATOR_PROMPT)
    chain = prompt | structured_llm
    result = chain.invoke({"topic": topic, "max_analysts": max_analysts})
    return [a.model_dump() for a in result.analysts]