from pm_state import PMState
from llm_client import FAST_MODEL, QUALITY_MODEL, call_llm
from concurrent.futures import ThreadPoolExecutor
import functools

def trim(text, max_chars=250):
    return text[:max_chars] if text else ""

@functools.lru_cache(maxsize=256)
def run_fast(prompt, model):
    return call_llm(prompt, model)

def run_orchestrator(idea, docs, max_docs=5):
    state = PMState(idea_text=idea)

    idea_words = set(idea.lower().split())

    def score_doc(d):
        text = (d.get("title","") + " " + d.get("content","")).lower()
        return (sum(w in text for w in idea_words), d)

    with ThreadPoolExecutor() as exe:
        scored = list(exe.map(score_doc, docs))

    top_docs = [d for _, d in sorted(scored, key=lambda x: x[0], reverse=True)[:max_docs]]

    state.context_sources = [
        {"title": d.get("title", "Untitled"), "id": f"doc-{i}"}
        for i, d in enumerate(top_docs)
    ]

    context_text = "\n".join(trim(d.get("content", "")) for d in top_docs)

    context_prompt = f"Summarize the following content:\n{context_text}"
    ctx = run_fast(context_prompt, FAST_MODEL)
    state.context_snippets.append(ctx)

    prd_prompt = f"Generate a structured PRD.\nIDEA:\n{idea}\n\nCONTEXT:\n{ctx}"
    state.prd_markdown = run_fast(prd_prompt, QUALITY_MODEL)

    return state
