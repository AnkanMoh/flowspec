import streamlit as st

def card(title, content, icon="🟦"):
    st.markdown(
        f"""
        <div style="
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
            background-color: #161B22;
            border: 1px solid #30363D;
        ">
            <h3 style="margin: 0; font-size: 20px;">{icon} {title}</h3>
            <p style="opacity: 0.85; margin-top: 10px; font-size: 15px; line-height: 1.6;">
                {content}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
