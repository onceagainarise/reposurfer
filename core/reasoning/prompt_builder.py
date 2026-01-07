def build_investigation_prompt(
    query: str,
    retrieved_symbols: list[dict],
) -> list[dict]:
    """
    Enhanced prompt builder for detailed analysis with specific locations and root cause
    """

    evidence_blocks = []
    for s in retrieved_symbols:
        snippet = s.get("text", "")[:800]  # Increased context
        evidence_blocks.append(
            f"""
Symbol: {s.get('id')}
Type: {s.get('type')}
File: {s.get('file')}
Line: {s.get('start_line', 'N/A')} - {s.get('end_line', 'N/A')}
Confidence: {s.get('confidence', 'N/A')}
---
{snippet}
""".strip()
        )

    evidence_text = "\n\n".join(evidence_blocks)

    system = {
        "role": "system",
        "content": (
            "You are a senior software engineer conducting a detailed code investigation. "
            "You MUST only use the provided code evidence. "
            "Provide specific, actionable insights with exact locations. "
            "If evidence is insufficient, explicitly state what's missing. "
            "Do not hallucinate code or files."
        ),
    }

    user = {
        "role": "user",
        "content": f"""
User Issue: {query}

ANALYSIS REQUIREMENTS:
1. **Root Cause Identification**: Identify the most likely root cause with specific evidence
2. **Exact Locations**: Provide precise file paths, line numbers, function/method names
3. **Detailed Explanation**: Explain WHY this issue occurs based on the code evidence
4. **Investigation Steps**: List specific steps to verify and fix the issue
5. **Related Components**: Mention other files/functions that might be affected

Relevant Code Evidence:
{evidence_text}

Format your response as:
## Root Cause Analysis
[Specific explanation with exact locations]

## Investigation Steps
1. **File**: [path] - [specific action]
   - Line: [numbers] - [what to check]
   
2. **File**: [path] - [specific action]
   - Line: [numbers] - [what to check]

## Why This Issue Occurs
[Detailed technical explanation based on evidence]

## Related Areas to Check
[List other potentially affected components]
""".strip(),
    }

    return [system, user]
