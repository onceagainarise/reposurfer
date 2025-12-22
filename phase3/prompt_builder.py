def build_explanation_prompt(query: str, evidence: list):
    prompt = f"""
You are a senior software engineer helping a contributor understand a codebase.  

User issue:
"{query}"

Below is a list of relevant code symbols retrieved from the repository.
Each item includes its type, file, and a snippet.

Your task:
- Explain why these symbols are relevant
- Suggest where the developer should start reading
- Do NOT invent files or functions
- Do NOT suggest fixes
- Stay grounded in the provided evidence

Evidence:
"""

    for i, e in enumerate(evidence, 1):
        prompt += f"""
[{i}]
Symbol: {e['id']}
Type: {e['type']}
File: {e['file']}
Snippet:
{e['snippet']}
"""

    prompt += """
Provide a concise explanation (5–8 sentences).
"""

    return prompt