# main.py
import streamlit as st
from dashboard.ui import run_dashboard

def main():
    # Configure Streamlit page settings
    st.set_page_config(page_title="GHG Emissions Dashboard", layout="wide")
    run_dashboard()

if __name__ == "__main__":
    main()