# dashboard/ui.py
import streamlit as st
import pandas as pd
import io
from calculator import calculate_emissions
from scada_client import get_scada_data
from report_parser import parse_pdf_report, parse_docx_report

def run_dashboard():
    st.title("Cement Plant GHG Emissions Dashboard")
    
    # Sidebar: File uploader for operations reports (PDF or DOCX)
    st.sidebar.header("Upload Operations Report")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
    if uploaded_file is not None:
        # Process the uploaded file based on its type.
        if uploaded_file.type == "application/pdf":
            report_text = parse_pdf_report(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            report_text = parse_docx_report(uploaded_file)
        else:
            report_text = "Unsupported file type."
        st.sidebar.text_area("Extracted Report Text", report_text, height=200)
    
    st.header("Real-Time Emissions Data")
    
    # Get simulated (or live) SCADA data.
    scada_data = get_scada_data()
    
    # Load emission factors from CSV.
    try:
        emission_factors = pd.read_csv("sample_data/emission_factors.csv")
    except Exception as e:
        st.error("Error loading emission factors data.")
        return
    
    # Calculate emissions using our two-tier logic.
    emissions_df = calculate_emissions(scada_data, emission_factors)
    
    # Display a table of emissions by scope.
    st.subheader("Emissions by Scope")
    st.dataframe(emissions_df)
    
    # KPI: Display total emissions.
    total_emissions = emissions_df['Emissions_kg_CO2e'].sum()
    st.metric("Total Emissions (kg CO₂e)", f"{total_emissions:.2f}")
    
    # Simulate an emissions trend chart.
    trend_data = {
        "Time": [scada_data.get("timestamp", "")] * 5,
        "Total Emissions": [total_emissions * factor for factor in [0.8, 0.9, 1.0, 1.1, 1.2]]
    }
    trend_df = pd.DataFrame(trend_data)
    st.subheader("Emissions Trend")
    st.line_chart(trend_df.set_index("Time"))
    
    # Report export options: Excel export (PDF export is under development).
    st.subheader("Export Reports")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export as Excel"):
            towrite = io.BytesIO()
            emissions_df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            st.download_button(
                label="Download Excel",
                data=towrite,
                file_name="emissions_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    with col2:
        if st.button("Export as PDF"):
            st.info("PDF export functionality is under development.")
