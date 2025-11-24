from typing import Optional, List, Dict
from pm_state import PMState
from llm_client import call_llm

def rank_docs(idea_text: str, docs: List[Dict[str, str]]):
    idea_tokens = set(idea_text.lower().split())
    scored = []

    for d in docs:
        text = (d.get("title", "") + " " + d.get("content", "")).lower()
        score = len(idea_tokens & set(text.split()))
        scored.append((score, d))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for score, d in scored]

def build_context(idea: str, docs: List[Dict[str, str]], max_docs=5):
    ranked = rank_docs(idea, docs)
    selected = ranked[:max_docs]

    lines = []
    for d in selected:
        lines.append(f"- {d.get('title')} — {d.get('content','')[:200]}")

    return "\n".join(lines), selected

def run_orchestrator(idea_text, local_docs, max_docs=5, user_id="demo-user"):
    state = PMState(user_id=user_id, idea_text=idea_text)

    summary, selected_docs = build_context(idea_text, local_docs, max_docs)
    state.context_sources = [
        {"title": d.get("title"), "url": d.get("url",""), "id": f"local-{i}"}
        for i, d in enumerate(selected_docs)
    ]

    context_prompt = f"""
    You are FlowSpec, a product research agent.

    IDEA:
    {idea_text}

    RELEVANT CONTEXT:
    {summary}

    Provide:
    - high-level context
    - conflicts or overlaps
    - 5 key PM clarifying questions
    """

    context_response = call_llm(context_prompt)
    state.context_snippets.append(context_response)

    prd_prompt = f"""
    Write a complete PRD based on this idea and context.

    IDEA:
    {idea_text}

    CONTEXT:
    {context_response}

    Follow structure:
    # Title
    # Summary
    # Problem Statement
    # Goals & Non-Goals
    # Users & Use Cases
    # Requirements
    ## Functional
    ## Non-functional
    # Risks
    # Open Questions
    """

    state.prd_markdown = call_llm(prd_prompt)
    return state
