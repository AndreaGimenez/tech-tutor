from ask_tutor import ask_tutor
import streamlit as st

st.title("💡 AI Code Explainer")

user_code = st.text_area("Paste your code here:")

if st.button("Explain Code"):
    if not user_code.strip():
        st.warning("Please enter some code first!")
    else:
        st.info("💭 Thinking...")
        
        stream = ask_tutor(user_code)
        response = ""
        placeholder = st.empty()
        for chunk in stream:
            response += chunk.choices[0].delta.content or ""
            placeholder.markdown(response)