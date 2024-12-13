import streamlit as st
import pandas as pd
import snowflake.connector

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

# Maintain state for patient ID
if "patient_id" not in st.session_state:
    st.session_state["patient_id"] = ""

if "admission_id" not in st.session_state:
    st.session_state["admission_id"] = None

st.title("Admissions & Discharge Analysis")
st.write("Enter the Patient ID to view admission records.")

# Input for Patient ID with session state
patient_id = st.text_input(
    "Patient ID",
    value=st.session_state["patient_id"],
    help="Enter the unique Patient ID.",
)

if patient_id:
    # Save patient_id to session_state
    st.session_state["patient_id"] = patient_id

    # Fetch Admission Details for Patient
    conn = connect_to_snowflake()
    query = f"""
        SELECT ADM_ADMISSION_ID, ADM_ADMIT_TIME, ADM_DISCH_TIME, LENGTH_OF_STAY
        FROM DIM_ADMISSIONS
        WHERE SUBJECT_ID = {patient_id}
        ORDER BY ADM_ADMIT_TIME DESC;
    """
    admissions_df = pd.read_sql(query, conn)
    conn.close()

    if admissions_df.empty:
        st.warning(f"No admissions found for Patient ID: {patient_id}.")
    else:
        st.write(f"Admissions for Patient ID: {patient_id}")
        st.dataframe(admissions_df)

        # Sorting Options
        sort_option = st.selectbox(
            "Sort admissions by:",
            options=["Most Recent Admission Time", "Most Recent Discharge Time"],
        )
        if sort_option == "Most Recent Discharge Time":
            admissions_df = admissions_df.sort_values("ADM_DISCH_TIME", ascending=False)

        # Admission Selection
        admission_id = st.selectbox(
            "Select Admission ID for Detailed Analysis:",
            options=admissions_df["ADM_ADMISSION_ID"],
            index=0 if st.session_state["admission_id"] is None else
            admissions_df["ADM_ADMISSION_ID"].tolist().index(st.session_state["admission_id"]),
        )

        if st.button("Detailed Admission Analysis"):
            # Save selected admission_id to session_state
            st.session_state["admission_id"] = admission_id
            st.success(f"Selected Admission ID: {admission_id}")
            st.switch_page("pages/2_admission_details.py")

        if st.button("Detailed Discharge Analysis"):
            # Save selected admission_id to session_state
            st.session_state["admission_id"] = admission_id
            st.success(f"Selected Admission ID: {admission_id}")
            st.switch_page("pages/3_discharge_details.py")

# Add Refresh Button
if st.button("Refresh"):
    # Clear Session State for Patient and Admission Data
    st.session_state["patient_id"] = None
    st.session_state["admission_id"] = None
    #st.experimental_rerun()