print("App started, imports working...")

import streamlit as st
import pandas as pd

from modules.data_fetcher import get_stock_history
from modules.analytics import compute_metrics
from modules.comparator import compare_two
from modules.ml_engine import cluster_stocks
from modules.genai_engine import generate_ai_answer



st.set_page_config(page_title="OptiML", layout="wide")

st.title("OptiML: Intelligent Financial Insights & Competitor Comparison Using GenAI")

tab1, tab2, tab3, tab4 = st.tabs(["Stock Analysis", "Compare Stocks", "ML Insights", "Ask AI"])

with tab1:
    symbol = st.text_input("Enter Stock Symbol:", "TCS.NS")
    if st.button("Analyze"):
        df = get_stock_history(symbol)
        st.line_chart(df.set_index("Date")["Close"])
        st.write("Metrics:", compute_metrics(df))

with tab2:
    s1 = st.text_input("Stock 1:", "TCS.NS")
    s2 = st.text_input("Stock 2:", "INFY.NS")
    if st.button("Compare"):
        df1 = get_stock_history(s1)
        df2 = get_stock_history(s2)
        st.write(compare_two(df1, df2, s1, s2))

with tab3:
    stock_list = ["TCS.NS", "INFY.NS", "HDFCBANK.NS", "RELIANCE.NS"]
    results = []
    for s in stock_list:
        hist = get_stock_history(s)
        metrics = compute_metrics(hist)
        metrics["symbol"] = s
        results.append(metrics)

    df = pd.DataFrame(results)
    st.subheader("Base metrics for selected stocks")
    st.dataframe(df)

    clustered = cluster_stocks(df)
    st.subheader("Clustered stocks (risk/return groups)")
    st.dataframe(clustered)


with tab4:
    st.subheader("Ask a financial question")

    question = st.text_area("Ask about risk/return, comparison, etc.")
    default_symbol = "TCS.NS"
    symbol_for_context = st.text_input(
        "Optional: symbol to use for context (for metrics)", default_symbol
    )

    if st.button("Ask AI"):
        # Build simple context using metrics of the chosen symbol
        hist = get_stock_history(symbol_for_context)
        base_metrics = compute_metrics(hist)

        st.write("Context metrics used for AI:", base_metrics)

        answer = generate_ai_answer(question, base_metrics)
        st.markdown("### 🔹 AI Financial Insight")
        st.write(answer)

