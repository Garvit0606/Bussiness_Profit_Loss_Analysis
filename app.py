import streamlit as st
import pandas as pd

from database import init_db
from auth import signup, login
from payments import get_payment_message
from analytics import (
    overall_metrics,
    time_based,
    profit_loss_bar,
    profit_loss_pie,
    total_sell_chart,
    top_products
)

# CONFIG 
ADMIN_EMAIL = "garvit.2003singhal@gmail.com"

st.set_page_config(
    page_title="Business Profit & Loss Analyzer",
    layout="wide"
)

# Init database (auto create table)
init_db()

st.title("Business Profit & Loss Analyzer")

# AUTH 
if "user" not in st.session_state:

    tab1, tab2 = st.tabs(["Login", " Signup"])

    # LOGIN 
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login(email, password)
            if user is not None:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid email or password")

    # SIGNUP 
    with tab2:
        email2 = st.text_input("Signup Email", key="signup_email")
        password2 = st.text_input("Signup Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            signup(email2, password2)
            st.success("Account created. Please login.")

# DASHBOARD 
else:
    # user tuple → (email, password, plan, expiry)
    email, password, plan, expiry = st.session_state.user

    # ADMIN OVERRIDE
    if email == ADMIN_EMAIL:
        plan = "PRO"
        expiry = "2099-12-31"

    st.success(f"Logged in as **{email}** | Plan: **{plan}**")

    st.markdown("---")

    # FILE UPLOAD 
    file = st.file_uploader(
        "Upload CSV / Excel File",
        type=["csv", "xlsx"]
    )

    if file is not None:
        try:
            # Load file
            if file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)

            # OVERALL METRICS 
            revenue, profit, loss, total_sell = overall_metrics(df)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Revenue", f"₹{revenue:,.2f}")
            c2.metric("Total Profit", f"₹{profit:,.2f}")
            c3.metric("Total Loss", f"₹{loss:,.2f}")
            c4.metric("Total Sell", total_sell)

            st.markdown("---")

            # PERIOD SELECT 
            period = st.radio(
                "Select Analysis Period",
                ["Weekly", "Monthly", "Yearly"],
                horizontal=True
            )

            period_key = period.lower()
            period_df = time_based(df, period_key)

            if period_df is not None and plan == "PRO":
                st.subheader(f"📅 {period} Profit / Loss")

                st.plotly_chart(
                    profit_loss_bar(period_df),
                    use_container_width=True
                )

                st.plotly_chart(
                    profit_loss_pie(period_df),
                    use_container_width=True
                )

            elif plan != "PRO":
                st.warning("Weekly / Monthly / Yearly analysis is PRO feature")
                st.info(get_payment_message())

            st.markdown("---")

            # TOTAL SELL CHART 
            st.subheader("Total Sell Analysis")
            sell_chart = total_sell_chart(df)
            if sell_chart is not None:
                st.plotly_chart(sell_chart, use_container_width=True)

            st.markdown("---")

            # MOST SELLING PRODUCT 
            st.subheader("Most Selling Products")
            bar, pie = top_products(df)
            if bar is not None and pie is not None:
                st.plotly_chart(bar, use_container_width=True)
                st.plotly_chart(pie, use_container_width=True)

        except Exception:
            st.warning("File uploaded, but analysis could not be completed.")
            st.info("Please upload a valid business data file with numeric values.")

    st.markdown("---")

    # LOGOUT 
    if st.button("Logout"):
        del st.session_state.user
        st.rerun()
