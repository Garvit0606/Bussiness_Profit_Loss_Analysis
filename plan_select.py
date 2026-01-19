import streamlit as st
from datetime import datetime, timedelta
from payments import get_payment

def plan_page():
    st.title("Choose Your Plan")

    if st.button("🆓 5 Days Free Trial"):
        st.session_state.plan = "TRIAL"
        st.session_state.expiry = datetime.now() + timedelta(days=5)
        st.rerun()

    st.markdown("---")

    for plan in ["MONTHLY", "YEARLY"]:
        upi, amt = get_payment(plan)
        st.subheader(f"{plan} PLAN – ₹{amt}")
        st.code(upi)
        paid = st.checkbox(f"I have paid for {plan}", key=plan)

        if paid:
            st.session_state.plan = plan
            st.session_state.expiry = datetime.now() + timedelta(
                days=30 if plan == "MONTHLY" else 365
            )
            st.success("Plan activated")
            st.rerun()
