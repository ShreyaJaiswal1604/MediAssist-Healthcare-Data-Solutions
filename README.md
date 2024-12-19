---

# 🌟  MediAssist Healthcare Data Solutions 🏥💻

MediAssist is a comprehensive healthcare solution that leverages advanced data engineering and AI capabilities to enhance medical coding accuracy and improve patient outcomes through risk stratification. By utilizing the MIMIC-IV dataset, MediAssist establishes a robust pipeline for ingesting, transforming, and analyzing healthcare data, culminating in an intuitive UI for clinicians to access actionable insights.

---
## 🌐 Live Demo

Experience **MediAssist AI** in action on Streamlit:  
[👉 Click here to access the application!](https://mediassist-ai.streamlit.app/)

Explore the features and capabilities of our application designed to enhance healthcare workflows and decision-making.

---

## 🎥 Demo Video

Watch the demo video showcasing MediAssist in action:

https://github.com/user-attachments/assets/d677b252-4877-4ad1-9a10-8620dae5a785


---
## 📊 Dataset: MIMIC-IV 🩺

MIMIC-IV is a publicly available dataset that includes comprehensive de-identified healthcare information. It is extensively used in the medical research and data science community for developing machine learning models and healthcare solutions.

- **Content**: Includes patient admissions, discharge summaries, clinical notes, and diagnosis data.
- **Version**: 3.1
- **Access**: [MIMIC-IV Dataset](https://physionet.org/content/mimiciv/3.1/)

> ⚠️ **Note**: Access to the dataset requires credentialed approval and adherence to ethical guidelines.

---

## 📌 Project Details

**MediAssist** focuses on:
- Accurate **ICD-10 code generation** for clinical notes.
- Concise **clinical note summarization**.
- Effective **patient risk stratification** to identify high-risk cases.
- A user-friendly **Streamlit UI** for real-time clinician insights.

---

## 🛠️ Tools and Technologies

| **Category**          | **Tools/Technologies**                                                                 |
|-----------------------|---------------------------------------------------------------------------------------|
| **Programming**        | Python 🐍                                                                            |
| **Data Engineering**   | Snowflake ❄️, DBT 🔄                                                                   |
| **AI Models**          | Hugging Face 🤗, Vertex AI 🎯, Llama Models 🦙 , Bert Models                                        |
| **Visualization/UI**   | Streamlit 🌐                                                                          |
| **Dataset**            | MIMIC-IV 🩺                                                                            |
| **PDF Generation**     | FPDF 📄                                                                               |

---

## 🏗️ Project Architecture

![Architecture Diagram](https://github.com/ShreyaJaiswal1604/MediAssist-Healthcare-Data-Solutions/blob/main/images/Final-architecture%20-image.jpeg)  
**"MediAssist Healthcare Data Workflow: From Raw Ingestion to Clinician Insights"**

### Workflow:
1. **Raw Data Ingestion**: MIMIC-IV data is loaded into the Snowflake **raw layer**.
2. **Data Transformation**: DBT processes and transforms raw data into a **staging layer**.
3. **Dimension Modeling**:
   - ICD-10 codes are generated via:
     1. Hugging Face serverless token.
     2. Vertex AI model deployment.
   - Clinical note summarization and risk stratification results are loaded into the dimension model.
4. **Fact and Dimension Layers**: Finalized data is stored in **facts and dimensions** for analysis.
5. **UI Layer**: A Streamlit-based application provides clinicians real-time access to patient insights.

---
## 🎨 Dimensional Modeling Diagram

Below is the dimensional modeling diagram representing the MediAssist data architecture:

![Dimensional Modeling Diagram](https://github.com/ShreyaJaiswal1604/MediAssist-Healthcare-Data-Solutions/blob/main/images/Architecture.png)

#### **Key Components:**

1. **Fact Tables**:
   - **FCT_NOTE_SUMMARIZATION**:
     - Central to summarizing patient history.
     - Links patient admission details, discharge notes, and pharmacy data.
   - **FCT_RISK_STRATIFICATION**:
     - Focuses on assessing patient risk levels.
     - Stores information about risk levels tied to diagnoses.
   - **FCT_MEDICAL_CODING**:
     - Facilitates medical coding operations.
     - Links diagnosis and procedure codes with medical records.

2. **Dimension Tables**:
   - **DIM_ADMISSIONS**:
     - Contains patient admission details such as admission/discharge time, race, insurance, and length of stay.
   - **DIM_PHARMACY**:
     - Captures pharmacy-related data, including prescribed medication and its frequency.
   - **DIM_DISCHARGE**:
     - Includes discharge summaries, timestamps, and subject-related information.
   - **DIM_ORG_CODES**:
     - Holds organizational code descriptions, severity levels, and mortality indicators.
   - **DIM_MEDICAL_CODES**:
     - Stores diagnostic and procedure codes with related metadata.
   - **DIM_ICD_DIAGNOSES_PROCEDURES**:
     - Contains ICD codes, descriptions, and flags for diagnoses and procedures.

---

#### **Primary Use Cases:**

1. **Patient History Summarization**:
   - Links data from:
     - **DIM_ADMISSIONS**: Admission-related details.
     - **DIM_PHARMACY**: Medication details.
     - **FCT_NOTE_SUMMARIZATION**: Summarizes patient interactions.

2. **Patient Risk Stratification**:
   - Combines:
     - **FCT_RISK_STRATIFICATION**: Records patient risk levels.
     - **DIM_ORG_CODES**: Risk severity and mortality indicators.

3. **Medical Coding**:
   - Integrates:
     - **FCT_MEDICAL_CODING**: Core table for medical coding.
     - **DIM_MEDICAL_CODES**: Diagnostic codes and metadata.
     - **DIM_ICD_DIAGNOSES_PROCEDURES**: ICD details for comprehensive reporting.

---

### 🌟 Analysis

This dimensional model ensures efficient data organization to support healthcare analytics and decision-making. It enables clinicians to:

- Summarize patient history for improved care continuity.
- Identify high-risk patients for timely interventions.
- Streamline medical coding for accurate billing and reporting.

---

## 🌟 Project Application

The **MediAssist UI** empowers healthcare providers to:
- **Retrieve patient admissions and discharge details.**
- **Analyze clinical note summaries.**
- **View ICD-10 medical codes with descriptions.**
- **Assess patient risk stratification metrics.**

---

## ✨ Main Features

- **Medical Code Generation**: Extract ICD-10 codes from clinical notes for documentation and billing.
- **Clinical Note Summarization**: Concise summaries for quicker decision-making.
- **Risk Stratification**: Identify high-risk patients for timely intervention.
- **Report Generation**: Generate and download detailed admission/discharge reports in PDF format.
- **Real-Time Insights**: Navigate patient data seamlessly through an intuitive UI.

---

## 🛠️ Installation and Setup

### 🖥️ Prerequisites

- Python 3.8 or later
- Virtual environment tools (`virtualenv`)
- Required Python packages: `snowflake-connector-python`, `fpdf`, `streamlit`, etc.

---

### ⚙️ Setup Guide

#### **1. Clone the Repository**
```bash
git clone https://github.com/ShreyaJaiswal1604/MediAssist-Healthcare-Data-Solutions.git
cd MediAssist-Healthcare-Data-Solutions
```

#### **2. Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt

```

#### **4. Configure DBT**
- Add your profiles.yml configuration for Snowflake:
```bash
my_dbt_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your_account>
      user: <your_username>
      password: <your_password>
      role: <your_role>
      database: mimic_iv_medi_assist
      warehouse: <your_warehouse>
      schema: prod_mimic
      threads: 4
      client_session_keep_alive: False

```
#### **5. Run DBT Models**
```bash
cd dbt
dbt run
```


#### **6. Launch the Streamlit Application**
```bash
streamlit run app.py
```

#### **7. Generate DBT Documentation**
```bash
dbt docs generate
dbt docs serve
```

#### **7. Generate DBT Documentation**
```bash
* Navigate to the Discharge Details page.
* Enter the patient and admission IDs.
* View the report details.
* Click Generate PDF Report to download a well-formatted report.
```


## 🚀 Future Enhancements

- 🌐 **Integration with External EHR Systems**: Enable real-time updates and seamless data flow.
- 📊 **Advanced Analytics Dashboards**: Provide deeper insights and enhance decision-making.
- 🩺 **Additional Use Cases**: Explore models for disease prediction and other advanced healthcare solutions.

---

## 🤝 Contribution

We welcome contributions! Feel free to fork this repository, make improvements, and raise pull requests. Together, let's build a better healthcare solution. 💡

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details. 📜
