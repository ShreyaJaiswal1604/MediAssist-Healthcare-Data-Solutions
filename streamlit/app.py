import streamlit as st
import base64

# Set page configuration
st.set_page_config(page_title="MediAssist Healthcare Solutions", page_icon="🩺")

# Custom CSS for layout adjustments
st.markdown(
    """
    <style>
    .center-header {
        font-size: 40px;
        text-align: center;
        font-weight: bold;
        color: #4CAF50;  /* Customize the color */
        margin-bottom: -1500px;  /* Remove gap above the divider */
    }
    .content-space {
        margin-top: 30px;  /* Space after the image */
    }
    .description-text {
        text-align: left;
        font-size: 18px;
        color: white;
        line-height: 1.6;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(255, 255, 0, 0.2);  /* Green with 0.9 opacity */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page Header
st.markdown(
    """
    <div class="center-header">MediAssist Healthcare Solutions</div>
    """,
    unsafe_allow_html=True,
)

# Rainbow Divider
st.header("", divider="rainbow")

# Embed the GIF
gif_path = "images/main_pg.gif"  # Path to your GIF file
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/gif;base64,{base64.b64encode(open(gif_path, "rb").read()).decode()}" alt="Healthcare demo" style="width: 100%; height: auto;">
    </div>
    """,
    unsafe_allow_html=True,
)

# Add space after the image
st.markdown('<div class="content-space"></div>', unsafe_allow_html=True)

# Description with fixed background color
st.markdown(
    """
    <div class="description-text">
        MediAssist is a real-time healthcare platform designed to enhance patient data analysis and decision-making. 
        This application offers:
        <ul>
            <li><b>Medical Code Information:</b> Retrieve and review detailed ICD-10 codes linked to patient records for accurate documentation and billing.</li>
            <li><b>Clinical Note Summarization:</b> Generate concise summaries of discharge records, highlighting key medical insights for efficient analysis.</li>
            <li><b>Risk Stratification:</b> Identify high-risk patients based on critical metrics derived from discharge and diagnosis data.</li>
        </ul>
        Streamline hospital operations with actionable insights and efficient management of patient records.
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer Section


st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        © 2024 MediAssist Healthcare Solutions. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)



# Add a welcoming image
#st.image('images/hosp_main_01.jpg', caption="Efficient Healthcare Data Access", width=600)

# Set background image
# Sidebar Background Function
# Sidebar Background Function
# Sidebar Title
# Custom CSS for Sidebar Title
st.markdown(
    """
    <style>
    .sidebar-title {
        font-size: 24px; /* Adjust the font size */
        font-weight: bold; /* Bold text */
        text-align: center; /* Center alignment */
        color: white; /* Text color for visibility */
        color: #003366; /* Dark blue text for visibility */
        background-color: rgba(173, 216, 230, 0.8); /* Pastel blue background */
        padding: 10px; /* Add padding for spacing */
        margin-bottom: 15px; /* Add spacing below */
        border-radius: 8px; /* Rounded corners for modern look */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation Title with Custom Styling
st.sidebar.markdown('<div class="sidebar-title">MediAssist Navigation</div>', unsafe_allow_html=True)

# Sidebar Description
st.sidebar.markdown(
    """
    Explore the core features:
    - **Admissions & Discharge Details**: Retrieve detailed patient records.
    - **Medical Codes Generation**: Generate and analyze ICD-10 codes.
    - **Risk Stratification**: Evaluate patient risks for better care planning.
    """
)

# Additional Styling for the Sidebar
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] > div:first-child {
        padding: 20px;
        background-color: rgba(173, 216, 230, 0.8); /* Pastel blue background */
      
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# def set_sidebar_background_with_color():
#     """
#     Sets a custom pastel blue background for the Streamlit sidebar and styles the buttons.
#     """
#     st.markdown(
#         """
#         <style>
#         /* Sidebar background styling */
#         [data-testid="stSidebar"] > div:first-child {
#             background-color: rgba(173, 216, 230, 0.8); /* Pastel blue with slight opacity */
#             padding: 20px; /* Add padding for better spacing */
#         }

#         /* Center align buttons */
#         .sidebar-buttons {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#         }

#         /* Style the buttons in the sidebar */
#         .stButton button {
#             background-color: #FF7F7F; /* Light red button color */
#             color: white;
#             border-radius: 12px; /* Rounded corners */
#             padding: 12px 24px;
#             margin: 10px 0; /* Add spacing between buttons */
#             font-size: 18px; /* Larger text for better visibility */
#             font-weight: bold; /* Bold text */
#             border: none;
#             transition: background-color 0.3s ease, color 0.3s ease; /* Smooth hover effect */
#         }

#         /* Button hover effect */
#         .stButton button:hover {
#             background-color: #90EE90; /* Light green on hover */
#             color: black; /* Text color changes to black */
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # Apply Sidebar Styling
# set_sidebar_background_with_color()

# # Custom CSS for Sidebar Title Background
# st.markdown(
#     """
#     <style>
#     .sidebar-title {
#         font-size: 22px; /* Adjust the font size */
#         font-weight: bold;
#         text-align: center;
#         padding: 10px;
#         margin-bottom: 10px;
#         color: #003366; /* Dark blue text for visibility */
#         background-color: rgba(173, 216, 230, 0.8); /* Pastel blue background */
        
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Sidebar Navigation
# st.sidebar.markdown('<div class="sidebar-title">MediAssist Navigation</div>', unsafe_allow_html=True)

# st.sidebar.write("Select a section below to access specific healthcare data and insights:")


# # Center the buttons
# st.sidebar.markdown('<div class="sidebar-buttons">', unsafe_allow_html=True)

# # Add buttons with nice spacing and hover effects
# if st.sidebar.button("Admissions & Discharge Details"):
#     st.experimental_set_query_params(page="1_admissions_discharge")
#     st.write("Navigate using the sidebar instead!")

# if st.sidebar.button("Medical Codes Generation"):
#     st.write("Navigated to Medical Codes Generation Page.")

# if st.sidebar.button("Risk Stratification"):
#     st.write("Navigated to Risk Stratification Page.")

# st.sidebar.markdown('</div>', unsafe_allow_html=True)


