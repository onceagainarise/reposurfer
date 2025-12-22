from phase3.snippet_extractor import SnippetExtractor
from phase3.prompt_builder import build_explanation_prompt
from phase3.llm_client import LLMClient



def run_phase3(repo_path, query, retrieved):
    extractor = SnippetExtractor(repo_path)
    llm = LLMClient()

    evidence = []
    for r in retrieved[:5]:
        snippet = extractor.extract(r["file"])
        evidence.append({
            "id": r["id"],
            "type": r["type"],
            "file": r["file"],
            "score": r["score"],
            "snippet": snippet            
        })
    
    prompt = build_explanation_prompt(query, evidence)
    explanation = llm.explain(prompt)
