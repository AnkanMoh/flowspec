import streamlit as st
from agents import run_orchestrator
from components.cards import card

st.title("Generate PRD")
st.caption("FlowSpec analyzes your database and creates a contextual PRD.")

docs = st.session_state.get("flowspec_docs")

if not docs:
    st.warning("Please upload a database first from the 📂 Upload Database page.")
    st.stop()

idea = st.text_area(
    "Describe your feature idea",
    height=200,
    placeholder="Example: Allow users to manage multiple saved payment methods…"
)

mode = st.radio("Mode", ["Speed", "Quality"], index=0)

if st.button("Generate PRD"):
    with st.spinner("FlowSpec is analyzing and generating your PRD..."):
        state = run_orchestrator(idea, docs, max_docs=5)

        st.subheader("📄 Generated PRD")
        st.markdown(state.prd_markdown)

        st.subheader("🔍 Research Context")
        for snippet in state.context_snippets:
            card("Context Summary", snippet)

        st.subheader("Related Documents")
        for src in state.context_sources:
            card(src["title"], "Source Document")

