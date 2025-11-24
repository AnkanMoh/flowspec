import streamlit as st
import pandas as pd
import io
from components.cards import card

st.title("📂 Upload Your Database")
st.caption("Upload your CSV workspace to help FlowSpec understand your product context.")

uploaded = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded:
    data = uploaded.read()
    df = pd.read_csv(io.BytesIO(data))

    st.success(f"Uploaded {len(df)} rows!")
    st.dataframe(df.head())

    # Save to session state
    st.session_state["flowspec_docs"] = df.to_dict(orient="records")

    card(
        "Next Step",
        "Navigate to the ** Generate PRD** page to use this database.",
        "➡️"
    )
