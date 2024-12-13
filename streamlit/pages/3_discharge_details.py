import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
import snowflake.connector
from fpdf import FPDF
from io import BytesIO
from datetime import datetime


# Snowflake connection setup
def connect_to_snowflake():
    return snowflake.connector.connect(
        user="DOLPHIN",
        password="Maapaa@1603",
        account="URB63596",
        warehouse="ANIMAL_TASK_WH",
        database="MIMIC_IV_MEDI_ASSIST",
        schema="PROD_MIMIC",
    )


# Fetch discharge record ID using Admission ID
def fetch_discharge_record_id(admission_id):
    query = f"""
    SELECT DIS_RECORD_ID
    FROM DIM_DISCHARGE
    WHERE DIS_HADM_ID = {admission_id};
    """
    conn = connect_to_snowflake()
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Fetch discharge details for the given discharge record ID
def fetch_discharge_details(dis_record_id):
    query = f"""
    SELECT *
    FROM DIM_DISCHARGE
    WHERE DIS_RECORD_ID = {dis_record_id};
    """
    conn = connect_to_snowflake()
    with conn.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
    conn.close()
    return pd.DataFrame(results, columns=columns) if results else None


# Fetch ICD codes and their descriptions
def fetch_icd_codes_with_descriptions(dis_record_id):
    query = f"""
    SELECT 
        llm.DMC_ICD_CODE AS icd_code,
        icd.ICD_LONG_TITLE AS description,
        icd.ICD_VERSION AS version,
        icd.ICD_TYPE AS icd_type
    FROM 
        DIM_MEDICAL_CODES_LLM AS llm
    JOIN 
        DIM_ICD_DIAGNOSES_PROCEDURES AS icd
    ON 
        llm.DMC_ICD_CODE = icd.ICD_CODE
    WHERE 
        llm.DIS_RECORD_ID = {dis_record_id};
    """
    conn = connect_to_snowflake()
    with conn.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    conn.close()
    return [
        {
            "ICD Code": row[0],
            "Description": row[1],
            "Version": row[2],
            "Type": row[3],
        }
        for row in results
    ]




class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "MediAssist Healthcare Solutions", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="C")

    def add_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def add_table(self, data, headers=None, col_widths=None):
        self.set_font("Arial", size=10)
        if headers:
            self.set_fill_color(200, 220, 255)  # Light blue background
            for i, header in enumerate(headers):
                self.cell(col_widths[i], 8, header, border=1, align="C", fill=True)
            self.ln()
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 8, str(cell), border=1, align="C")
            self.ln()

    def add_paragraph(self, text):
        self.set_font("Arial", size=10)
        self.multi_cell(0, 8, text)
        self.ln(5)


def generate_pdf_report(discharge_details, medical_codes, dis_record_id):
    pdf = PDF()
    pdf.add_page()

    # Title Section
    pdf.add_title(f"Discharge Report for Record ID: {dis_record_id}")

    # Discharge Details Table
    pdf.add_title("Discharge Details")
    discharge_table_data = [[key, val] for key, val in discharge_details.items()]
    pdf.add_table(discharge_table_data, headers=["Field", "Value"], col_widths=[50, 130])

    # Medical Codes Table
    if medical_codes:
        pdf.add_title("Medical Codes and Descriptions")
        medical_codes_table_data = [
            [code["ICD Code"], code["Description"], code["Version"], code["Type"]]
            for code in medical_codes
        ]
        pdf.add_table(
            medical_codes_table_data,
            headers=["ICD Code", "Description", "Version", "Type"],
            col_widths=[40, 100, 20, 30],
        )
    else:
        pdf.add_paragraph("No medical codes found for this discharge record.")

    # Save to BytesIO
    pdf_output = BytesIO()
    pdf.output(pdf_output, "S")  # Save to buffer
    pdf_output.seek(0)  # Reset pointer
    return pdf_output




# Streamlit App
st.title("Discharge Details")

# Ensure Patient ID and Admission ID are set
if not st.session_state.get("patient_id"):
    st.error("Patient ID is not set. Please go back to the previous page.")
    st.stop()

if not st.session_state.get("admission_id"):
    st.error("Admission ID is not set. Please go back to the previous page.")
    st.stop()

patient_id = st.session_state["patient_id"]
admission_id = st.session_state["admission_id"]

st.write(f"Patient ID: {patient_id}")
st.write(f"Admission ID: {admission_id}")

# Fetch discharge record ID
dis_record_id = fetch_discharge_record_id(admission_id)
if dis_record_id:
    st.success(f"Discharge Record ID Found: {dis_record_id}")

    # Fetch discharge details
    discharge_details_df = fetch_discharge_details(dis_record_id)
    if discharge_details_df is not None:
        st.subheader("Discharge Details")
        st.write(discharge_details_df)

        # Ask to view discharge summary
        if st.checkbox("View Discharge Summary"):
            st.subheader("Discharge Summary")
            summary = discharge_details_df.iloc[0]["DIS_NOTE_SUMMARY"]
            st.write(summary)

        # Ask to view medical codes
        if st.checkbox("View Associated Medical Codes"):
            medical_codes = fetch_icd_codes_with_descriptions(dis_record_id)
            if medical_codes:
                st.subheader("Medical Codes and Descriptions")
                st.write(pd.DataFrame(medical_codes))
            else:
                st.warning("No medical codes found for this discharge record.")

        # Generate report
    if st.button("Generate PDF Report"):
        discharge_details_dict = discharge_details_df.iloc[0].to_dict()
        pdf = generate_pdf_report(discharge_details_dict, medical_codes, dis_record_id)
        st.download_button(
            label="Download Discharge Report",
            data=pdf,
            file_name=f"Discharge_Report_{dis_record_id}.pdf",
            mime="application/pdf",
        )
    else:
        st.error("No discharge details found for the given Discharge Record ID.")
else:
    st.error("No discharge record found for the given Admission ID.")
