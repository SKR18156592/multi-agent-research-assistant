SUMMARIZE_INTERVIEW_PROMPT = """Summarize the key insights, evidence, and conclusions from this interview with {name}:
{messages}
"""

FINAL_REPORT_COMPILER_PROMPT = """You are a lead synthesis editor. Combine the following research briefs into a coherent, comprehensive final report on '{topic}'.
Ensure clear headings, citations/attributions, and an executive summary.

Research Briefs:
{sections}
"""