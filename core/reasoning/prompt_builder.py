def build_investigation_prompt(
    query: str,
    retrieved_symbols: list[dict],
) -> list[dict]:
    """
    retrieved_symbols: output of Phase 2 hybrid retriever
    """

    evidence_blocks = []
    for s in retrieved_symbols:
        snippet = s.get("text", "")[:500]
        evidence_blocks.append(
            f"""
Symbol: {s.get('id')}
Type: {s.get('type')}
File: {s.get('file')}
---
{snippet}
""".strip()
        )

    evidence_text = "\n\n".join(evidence_blocks)

    system = {
        "role": "system",
        "content": (
            "You are a senior software engineer assisting in code investigation. "
            "You MUST only use the provided code evidence. "
            "If something is missing, say so explicitly. "
            "Do not hallucinate code or files."
        ),
    }

    user = {
        "role": "user",
        "content": f"""
User problem:
{query}

Relevant code evidence:
{evidence_text}

Task:
1. Identify the most likely root cause area
2. List concrete investigation steps (files + what to look for)
3. Do NOT suggest fixes yet
""".strip(),
    }

    return [system, user]
