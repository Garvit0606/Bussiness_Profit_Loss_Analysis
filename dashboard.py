import streamlit as st
import pandas as pd
from analytics import clean_df, calculate_metrics, add_time, bar_chart, pie_chart

def dashboard():
    st.header("📊 Business Analytics Dashboard")

    file = st.file_uploader("Upload CSV / Excel / JSON", ["csv", "xlsx", "json"])
    if not file:
        return

    if file.name.endswith("csv"):
        df = pd.read_csv(file)
    elif file.name.endswith("xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_json(file)

    df = clean_df(df)
    revenue, cost, profit, total_sales = calculate_metrics(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", f"₹{revenue}")
    c2.metric("Cost", f"₹{cost}")
    c3.metric("Profit", f"₹{profit}")
    c4.metric("Total Sales", total_sales)

    df = add_time(df)

    if "date" in df.columns:
        st.plotly_chart(bar_chart(df, profit), use_container_width=True)
        st.plotly_chart(pie_chart(profit, cost), use_container_width=True)

        st.subheader("📅 Time-wise Profit")
        st.write("Weekly", df.groupby("week").sum(numeric_only=True))
        st.write("Monthly", df.groupby("month").sum(numeric_only=True))
        st.write("Yearly", df.groupby("year").sum(numeric_only=True))
