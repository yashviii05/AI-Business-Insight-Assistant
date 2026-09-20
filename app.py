"""
app.py
------
Phase 4: The interface. Run this file with:

    streamlit run app.py

Streamlit turns this plain Python script into a website automatically —
you don't need to write any HTML or JavaScript.
"""

import time
import streamlit as st

from nl_to_sql import ask_question
from summarize import summarize_results
from logger import log_query, calculate_success_rate

st.set_page_config(page_title="AI Business Insight Assistant", page_icon="📊")

st.title("📊 AI Business Insight Assistant")
st.write("Ask a question about your data in plain English — no SQL required.")

# --- Example question buttons (Phase 4, Step 5) ---
st.write("Try an example:")
example_questions = [
    "Which category has the highest stock-out risk?",
    "What are the top 5 discounted SKUs?",
    "What is the average price by category?",
]

# We store the chosen question in Streamlit's "session state" so it
# survives between button clicks and text box updates.
if "question" not in st.session_state:
    st.session_state.question = ""

cols = st.columns(len(example_questions))
for col, q in zip(cols, example_questions):
    if col.button(q):
        st.session_state.question = q

# --- Text box (Phase 4, Step 3) ---
question = st.text_input("Or type your own question:", value=st.session_state.question)

# --- Button to trigger everything (Phase 4, Step 4) ---
if st.button("Ask", type="primary") and question:
    start_time = time.time()

    with st.spinner("Thinking..."):
        sql_query, results, error = ask_question(question)

    elapsed = time.time() - start_time

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    if error:
        st.error(error)
        log_query(question, sql_query, success=False, elapsed_seconds=elapsed)
    else:
        st.subheader("Results")
        st.dataframe(results)

        with st.spinner("Summarizing..."):
            summary = summarize_results(question, results)
        st.subheader("Plain-English Answer")
        st.success(summary)

        log_query(question, sql_query, success=True, elapsed_seconds=elapsed)

# --- Show running accuracy metric (Phase 5) ---
st.sidebar.metric("Query success rate so far", f"{calculate_success_rate()}%")
