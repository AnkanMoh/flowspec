from llm_client import call_llm, FAST_MODEL, QUALITY_MODEL
from pm_state import PMState


def run_orchestrator(idea, docs, max_docs=5):
    state = PMState(idea_text=idea)

    ranked = sorted(
        docs,
        key=lambda d: sum(
            w in (d.get("title", "") + d.get("content", "")).lower()
            for w in idea.lower().split()
        ),
        reverse=True,
    )

    selected = ranked[:max_docs]
    state.context_sources = [{"title": d.get("title", "Untitled")} for d in selected]

    context_text = "\n".join([d.get("content", "")[:200] for d in selected])

    ctx_prompt = f"""
    You are FlowSpec, a product research agent.

    IDEA:
    {idea}

    RELEVANT DOC SNIPPETS:
    {context_text}

    Summarize:
    - main themes
    - likely overlaps/conflicts
    - 5 key questions a PM should ask before scoping this.
    """
    ctx = call_llm(ctx_prompt, model=FAST_MODEL)
    state.context_snippets.append(ctx)

    prd_prompt = f"""
    You are an experienced product manager.

    Write a clear, structured PRD.

    IDEA:
    {idea}

    CONTEXT (from internal docs):
    {ctx}

    Follow this structure:

    # Title
    # Summary
    # Problem Statement
    # Goals & Non-Goals
    # Users & Use Cases
    # Requirements
    ## Functional Requirements
    ## Non-Functional Requirements
    # Risks & Assumptions
    # Open Questions
    """

    state.prd_markdown = call_llm(prd_prompt, model=QUALITY_MODEL)
    return state
