import streamlit as st

##### Mainpage Content #####

# Header and Application Image

col1, col2 = st.columns([3, 2.5])

with col1:
    # Add the image in the first column
    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUHsukDlu-Hr8VrNSeS5tm1HRXa9iOXNRhhw&s"
    st.image(image_url, width=350)  # Specify the image width

with col2:
    # Add the headers next to the image
    st.title("MediAssist")
    st.subheader("An Innovative AI-driven healthcare solution")
    st.write("Created by Yash Pankhania, Shreya Jaiswal and Utkarsha Shirke")
    # Uncomment the following line if required:
    # st.write("Fox Chase Cancer Center")

# Add a horizontal line and then the summary section
st.markdown("---")
    
#########################################################################################

# Introduction
st.markdown("""
## Introduction

MediAssist revolutionizes healthcare delivery by leveraging AI-driven solutions to address key challenges in patient care and clinical operations. By focusing on streamlining workflows and enhancing decision-making, MediAssist integrates seamlessly into healthcare systems to improve efficiency, accuracy, and patient outcomes.

Whether you’re a clinician seeking quick insights into patient history, a medical coder aiming to optimize documentation, or a healthcare organization prioritizing high-risk patients, MediAssist provides the tools to drive better care through advanced automation and data analysis. This blog delves into its groundbreaking features, use cases, and potential to transform modern healthcare practices.
""")

# Divider
st.markdown("---")

##################################################################

# Product Features 

# Patient History Summarization

# Add two columns for text and image
col1, col2 = st.columns([3, 2])  # Adjust column proportions

with col1:
    st.write("""
    ## Product Features

    ### 1. Patient History Summarization

    Efficiently managing patient history is crucial for clinicians to provide accurate and timely care. MediAssist addresses this need by offering an AI-powered patient history summarization feature that consolidates extensive Electronic Health Records (EHRs) into a digestible format.

    #### Key functionalities include:
    - **Comprehensive Summarization:** MediAssist extracts critical details such as hospital visits, insurance information, prescribed medications, and lab results. It generates a concise yet thorough overview, eliminating the need to manually sift through lengthy EHRs.
    - **Clinical Note Summaries:** The system dives deeper into clinical notes, providing detailed yet structured insights into diagnoses, procedures, and treatment plans.
    - **Enhanced Decision-Making:** By delivering quick and relevant insights, clinicians can focus more on patient care, making faster and more informed decisions during consultations or emergencies.

    """)  

    with col2:
    # Increase the image size by setting the width parameter
        st.markdown("<div style='margin-top: 120px;'></div>", unsafe_allow_html=True)
        with st.container():
            st.image("https://github.com/user-attachments/assets/80b397a1-d937-4bc1-acda-9c60906bb5bb", 
                    caption="Patient Summarization Report", 
                    use_column_width=False, 
                    width=400)
            
st.write ("This feature significantly reduces the time spent on administrative tasks, enabling healthcare providers to prioritize patient engagement and improve care outcomes.")
        
# Divider
st.markdown("---")

###########################################################################################

# Medical Coding

# Add two columns for text and image
col1, col2 = st.columns([3, 2])  # Adjust column proportions

with col1:
   st.write("""
    ### 2. Medical Coding

    Medical coding is an essential but time-intensive process in healthcare. MediAssist transforms this traditionally manual task by automating the extraction and application of standardized ICD (International Classification of Diseases) codes from clinical documentation.

    #### Key functionalities include:
    - **Automated ICD Code Extraction and Application:**  
        MediAssist streamlines the medical coding process by automatically identifying and applying standardized ICD codes from detailed clinical notes. It ensures accuracy and consistency in capturing diagnoses and procedures, reducing the need for manual coding efforts.  

    - **Error Minimization and Administrative Efficiency:**  
        The system automates complex coding workflows, significantly reducing administrative burdens for healthcare providers. By minimizing the risk of coding errors, it helps prevent billing discrepancies and compliance issues, improving overall operational efficiency.
        """)   

with col2:
    # Increase the image size by setting the width parameter
    st.markdown("<div style='margin-top: 230px;'></div>", unsafe_allow_html=True)
    with st.container():
        st.image("https://github.com/user-attachments/assets/1089180b-c66a-418d-8db0-6eb9cd9bb85e", 
                caption="Patient Summarization Report", 
                use_column_width=False, 
                width=400)

st.write ("This feature significantly reduces the time spent on manual coding tasks, enabling healthcare providers to enhance billing accuracy and focus on delivering quality patient care.")

# Divider
st.markdown("---")

###############################################################################

# Risk Stratification

# Add two columns for text and image
col1, col2 = st.columns([2, 2])  # Adjust column proportions

with col1:
    st.write("""
### 3. Patient Risk Stratification

Early identification and prioritization of high-risk patients are essential for effective healthcare delivery. MediAssist uses AI-driven algorithms to analyze EHR data and categorize patients based on their risk levels, enabling healthcare providers to proactively address potential health issues.

#### Key functionalities include:
- **Risk Factor Analysis:** MediAssist evaluates a wide range of data points, including comorbidities, historical health records, and demographic information, to identify patients who may require immediate or enhanced care.
- **Preventative Care Support:** The system flags high-risk patients and highlights associated risk factors, allowing clinicians to implement preventative interventions and monitor conditions closely.
- **Resource Allocation:** By stratifying patients based on urgency, healthcare providers can allocate resources more effectively, ensuring that high-risk patients receive timely attention.


""")  

with col2:
    # Increase the image size by setting the width parameter
        st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)
        with st.container():
            st.image("https://github.com/user-attachments/assets/2250b957-d5a0-46ca-9175-c5f18890ca1f", 
                    caption="Risk Stratification Criteria", 
                    use_column_width=False, 
                    width=500)
            

st.write("This feature not only improves patient outcomes but also reduces the overall burden on healthcare systems by enabling proactive rather than reactive care.")

# Divider
st.markdown("---")

############################################################################################3

# The Future Section
st.markdown("""
## The Future of Healthcare with MediAssist

MediAssist is redefining healthcare workflows, making them faster, more accurate, and insight-driven. By automating time-intensive processes, enhancing clinical decision-making, and enabling targeted care, MediAssist empowers healthcare providers to focus on what truly matters—delivering exceptional patient care.

As the healthcare industry continues to evolve, solutions like MediAssist will play a pivotal role in bridging the gap between technology and patient-centric care. Stay tuned as we explore real-world applications and success stories that showcase MediAssist’s transformative impact.
""")


