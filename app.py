import streamlit as st
from backend import process_query

st.title("AI Smart Campus Assistant")

query = st.text_input("Ask your campus assistant")

if st.button("Submit"):
    if query:
        answer = process_query(query)
        st.write(answer)