
import streamlit as st
def check_plan(plan,expiry):
    if plan!="PRO":
        st.warning("Free Plan: Upgrade to unlock all features")
