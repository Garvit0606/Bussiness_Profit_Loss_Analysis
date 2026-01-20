import streamlit as st
import pandas as pd
from pathlib import Path

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

# ---------------- CONFIG ----------------
ADMIN_EMAIL = "garvit.2003singhal@gmail.com"

st.set_page_config(
    page_title="Business Profit & Loss Analyzer",
    layout="wide"
)

# ---------------- LOAD CSS ----------------
def load_css():
    css_file = Path("style.css")
    if css_file.exists():
        st.markdown(
            f"<style>{css_file.read_text()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ---------------- INIT DB ----------------
init_db()

st.title("📊 Business Profit & Loss Analyzer")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "plan_selected" not in st.session_state:
    st.session_state.plan_selected = False

# ======================================================
# ================= AUTH SECTION ========================
# ======================================================
if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

    # -------- LOGIN --------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

    # -------- SIGNUP --------
    with tab2:
        email2 = st.text_input("Signup Email", key="signup_email")
        password2 = st.text_input("Signup Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            signup(email2, password2)
            st.success("✅ Account created. Please login.")

# ======================================================
# ================= DASHBOARD ===========================
# ======================================================
else:
    # user tuple → (email, password, plan, expiry)
    email, password, plan, expiry = st.session_state.user

    # -------- ADMIN OVERRIDE --------
    if email == ADMIN_EMAIL:
        plan = "PRO"
        expiry = "2099-12-31"
        st.session_state.plan_selected = True

    # -------- PLAN SELECTION --------
    if not st.session_state.plan_selected and email != ADMIN_EMAIL:
        st.subheader("💳 Choose Your Plan")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🆓 Free Trial (5 Days)")
            if st.button("Start Free Trial"):
                st.session_state.plan_selected = True
                plan = "TRIAL"

        with col2:
            st.markdown("### 💼 Monthly Plan")
            st.write("₹999 / month")
            if st.button("Choose Monthly"):
                st.session_state.plan_selected = True
                plan = "PRO"

        with col3:
            st.markdown("### 🏆 Yearly Plan")
            st.write("₹9999 / year")
            if st.button("Choose Yearly"):
                st.session_state.plan_selected = True
                plan = "PRO"

        st.info(get_payment_message())
        st.stop()

    # -------- HEADER --------
    st.success(f"👤 Logged in as **{email}** | Plan: **{plan}**")
    st.markdown("---")

    # -------- FILE UPLOAD --------
    file = st.file_uploader(
        "📂 Upload CSV / Excel File",
        type=["csv", "xlsx"]
    )

    if file:
        try:
            if file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)

            # -------- OVERALL METRICS --------
            revenue, profit, loss, total_sell = overall_metrics(df)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Revenue", f"₹{revenue:,.2f}")
            c2.metric("Total Profit", f"₹{profit:,.2f}")
            c3.metric("Total Loss", f"₹{loss:,.2f}")
            c4.metric("Total Sell", total_sell)

            st.markdown("---")

            # -------- PERIOD ANALYSIS --------
            period = st.radio(
                "📅 Select Analysis Period",
                ["Weekly", "Monthly", "Yearly"],
                horizontal=True
            )

            period_key = period.lower()
            period_df = time_based(df, period_key)

            if plan == "PRO" and period_df is not None:
                st.subheader(f"{period} Profit / Loss")

                st.plotly_chart(
                    profit_loss_bar(period_df),
                    use_container_width=True
                )

                st.plotly_chart(
                    profit_loss_pie(period_df),
                    use_container_width=True
                )
            else:
                st.warning("⛔ Period-wise analysis is PRO feature")
                st.info(get_payment_message())

            st.markdown("---")

            # -------- TOTAL SELL --------
            st.subheader("📦 Total Sell Analysis")
            sell_chart = total_sell_chart(df)
            if sell_chart:
                st.plotly_chart(sell_chart, use_container_width=True)

            st.markdown("---")

            # -------- TOP PRODUCTS --------
            st.subheader("🔥 Most Selling Products")
            bar, pie = top_products(df)
            if bar and pie:
                st.plotly_chart(bar, use_container_width=True)
                st.plotly_chart(pie, use_container_width=True)

        except Exception as e:
            st.error("❌ File uploaded but analysis failed")
            st.code(str(e))

    st.markdown("---")

    # -------- LOGOUT --------
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
