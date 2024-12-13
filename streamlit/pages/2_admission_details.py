import streamlit as st
import pandas as pd
import snowflake.connector
from fpdf import FPDF
from datetime import datetime
import os

# Snowflake connection
def connect_to_snowflake():
    return snowflake.connector.connect(
        user="DOLPHIN",
        password="Maapaa@1603",
        account="URB63596",
        warehouse="ANIMAL_TASK_WH",
        database="mimic_iv_medi_assist",
        schema="prod_mimic",
    )

# Generate PDF Report with Formatting
def generate_pdf(patient_id, admission_id, admission_details):
    pdf = FPDF()
    pdf.add_page()

    # Add border to the page
    pdf.set_draw_color(0, 0, 128)  # Navy blue border
    pdf.rect(5.0, 5.0, 200.0, 287.0)  # Border dimensions

    # Branding and Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.set_text_color(0, 51, 102)  # Navy blue
    pdf.cell(0, 10, "MediAssist Healthcare Solutions", ln=True, align="C")
    pdf.ln(10)

    # Report Header
    pdf.set_font("Arial", style="BU", size=14)  # Bold + Underlined
    pdf.cell(0, 10, "Admission Details Report", ln=True, align="C")
    pdf.ln(10)

    # Patient ID and Admission ID Section
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)  # Black
    pdf.set_fill_color(230, 230, 250)  # Light lavender background
    pdf.cell(0, 10, f"Patient ID: {patient_id}", ln=True, fill=True, border=1)
    pdf.cell(0, 10, f"Admission ID: {admission_id}", ln=True, fill=True, border=1)
    pdf.ln(10)

    # Admission Details Section
    pdf.set_font("Arial", style="B", size=12)
    pdf.set_text_color(0, 51, 102)  # Navy blue
    pdf.cell(0, 10, "Admission Details:", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)  # Black
    for col, value in admission_details.items():
        pdf.cell(60, 10, f"{col.replace('_', ' ')}:", border=1, align="L")
        pdf.cell(130, 10, str(value), border=1, align="L")
        pdf.ln(10)

    # Timestamp at the bottom-right corner
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_y(-20)  # Position at the bottom
    pdf.set_font("Arial", style="I", size=10)
    pdf.set_text_color(128, 128, 128)  # Gray
    pdf.cell(0, 10, f"Report generated on: {timestamp}", align="R")

    # Save PDF to a temporary file
    pdf_path = f"Admission_Report_{admission_id}.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Check session_state for patient_id and admission_id
if "patient_id" not in st.session_state or "admission_id" not in st.session_state:
    st.error("No Patient ID or Admission ID found. Please go back and select a record.")
    st.stop()

patient_id = st.session_state["patient_id"]
admission_id = st.session_state["admission_id"]

st.title("Admission Details")
st.write(f"Displaying details for Admission ID: {admission_id} (Patient ID: {patient_id})")

# Fetch Admission Details
conn = connect_to_snowflake()
query = f"""
    SELECT *
    FROM DIM_ADMISSIONS
    WHERE ADM_ADMISSION_ID = {admission_id};
"""
admission_details_df = pd.read_sql(query, conn)
conn.close()

if not admission_details_df.empty:
    # Convert details to a dictionary for easy formatting
    admission_details = admission_details_df.iloc[0].to_dict()

    # Display Admission Details as a Form
    for col, value in admission_details.items():
        st.text_input(f"{col.replace('_', ' ')}:", value=str(value), disabled=True)

    # Generate and Download Report
    if st.button("Generate Admission Report"):
        pdf_path = generate_pdf(patient_id, admission_id, admission_details)
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.success("Report generated successfully!")
        st.download_button(
            label="Download Admission Report",
            data=pdf_data,
            file_name=f"Admission_Report_{admission_id}.pdf",
            mime="application/pdf",
        )
        os.remove(pdf_path)  # Clean up temporary file after download
else:
    st.warning(f"No details found for Admission ID: {admission_id}.")

if st.button("Go Back to Admissions & Discharge Page"):
    st.switch_page("pages/1_admission_discharge.py")
