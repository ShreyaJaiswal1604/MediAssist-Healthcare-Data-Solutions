# MediAssist Healthcare Data Solutions 🏥💻

MediAssist is a comprehensive healthcare solution that leverages advanced data engineering and AI capabilities to enhance medical coding accuracy and improve patient outcomes through risk stratification. By utilizing the MIMIC-IV dataset, MediAssist establishes a robust pipeline for ingesting, transforming, and analyzing healthcare data, culminating in an intuitive UI for clinicians to access actionable insights.

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

![Architecture Diagram](path/to/architecture_image.png)  
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
git clone https://github.com/your-username/MediAssist-Healthcare-Data-Solutions.git
cd MediAssist-Healthcare-Data-Solutions
