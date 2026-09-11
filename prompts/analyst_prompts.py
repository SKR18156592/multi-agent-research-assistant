ANALYST_PERSONA_GENERATOR_PROMPT = """You are tasked with creating a diverse panel of expert analysts to investigate the following topic:
Topic: {topic}

Generate up to {max_analysts} distinct expert personas. Each should have a distinct viewpoint, domain expertise, and angle of inquiry.
Return a structured list of analysts.
"""