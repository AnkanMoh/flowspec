import streamlit as st
from components.cards import card

st.set_page_config(
    page_title="FlowSpec — AI PM Copilot",
    page_icon="⚡",
    layout="wide"
)

st.title("FlowSpec")
st.caption("Your AI-powered PM Copilot")

st.write("")
st.subheader(" Quick Actions")

col1, col2 = st.columns(2)

with col1:
    card(
        "Upload your product database",
        "Import CSV files containing previous PRDs, project notes, and specs. FlowSpec will use this as your knowledge graph."
    )

with col2:
    card(
        "Generate a new PRD",
        "Turn any feature idea into a complete, structured, context-aware Product Requirements Document."
    )

st.subheader(" What FlowSpec Can Do")

card(
    "Contextual Research",
    "Automatically finds matching documents from your uploaded workspace and turns them into actionable context.",
    "🔍"
)

card(
    "Full PRD Generation",
    "Produces high-quality, structured PRDs with Goals, Problem Statement, Use Cases, Functional Requirements, Risks, and more.",
    "📄"
)

