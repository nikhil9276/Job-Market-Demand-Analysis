import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import logging
from io import StringIO
import os
import requests
import base64

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# --- Add Font Awesome for icons (Separate markdown block) ---
# This should be done early to ensure icons load correctly
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# Custom CSS for enhanced appearance (Dark Theme)
custom_css = """
<style>
/* Import Google Font - Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

body {
    background-color: #121212; /* Very dark background */
    color: #ffffff; /* White text */
    font-family: 'Inter', sans-serif; /* Use Inter font */
}
.stApp {
    max-width: 1200px; /* Max width for content */
    margin: 0 auto; /* Center the content */
    padding: 2.5rem; /* Add padding around content */
    background-color: #1f1f1f; /* Slightly lighter dark background for the app container */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.8); /* Stronger shadow for depth */
    border-radius: 15px; /* Rounded corners */
    color: #ffffff;
    display: flex;
    flex-direction: column;
    animation: fadeIn 1s ease-out; /* Fade in animation for the app container */
}

/* Keyframe Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes textShadow {
    from { text-shadow: 2px 3px 8px rgba(0, 0, 0, 0.4); }
    to { text-shadow: 3px 4px 12px rgba(0, 0, 0, 0.6); }
}

@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 0 10px rgba(168, 85, 247, 0.4); }
    50% { transform: scale(1.02); box-shadow: 0 0 20px rgba(168, 85, 247, 0.6); }
    100% { transform: scale(1); box-shadow: 0 0 10px rgba(168, 85, 247, 0.4); }
}

/* Title Styling */
h1 {
    color: #ffffff;
    text-align: center;
    font-size: 5rem; /* Slightly adjusted size */
    font-weight: 900; /* Bolder weight */
    background: linear-gradient(to right, #6366f1, #8b5cf6, #d946ef, #e879f9); /* Added more colors */
    -webkit-background-clip: text;
    color: transparent;
    background-size: 300% 300%;
    line-height: 1.2;
    margin-bottom: 2rem;
    letter-spacing: -0.03em; /* Tighter spacing */
    text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.6); /* Enhanced shadow */
    animation: gradientShift 4s ease-in-out infinite, textShadow 1.5s ease-in-out infinite alternate; /* Adjusted animation */
}

/* Subheading Styling */
h2, h3, h4 {
    color: #a78bfa; /* Lighter purple */
    animation: fadeIn 1.2s ease;
    font-weight: 700; /* Bold */
    margin-top: 3rem;
    margin-bottom: 1.5rem;
    border-bottom: 3px solid #a78bfa; /* Border color matches heading */
    padding-bottom: 0.6rem;
    letter-spacing: -0.01em;
}

/* KPI Container */
.kpi-container {
    display: flex;
    justify-content: space-evenly; /* Distribute space evenly */
    margin-bottom: 3rem; /* More space below KPIs */
    flex-wrap: wrap; /* Allow wrapping */
    gap: 20px; /* Add gap between items */
}

/* KPI Item Styling */
.kpi-item {
    background-color: #2d3748; /* Darker blue-gray background */
    padding: 2rem; /* Adjusted padding */
    border-radius: 15px;
    border: 2px solid #5a6375; /* Slightly lighter border */
    text-align: center;
    min-width: 250px; /* Increased minimum width */
    flex-grow: 1; /* Allow items to grow */
    animation: fadeIn 1s ease, pulse 3s infinite alternate; /* Adjusted pulse animation */
    transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); /* Initial shadow */
}
.kpi-item:hover {
    transform: translateY(-8px) scale(1.05); /* Lift and slightly scale on hover */
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.6); /* Stronger shadow on hover */
    background-color: #3a455a; /* Darker background on hover */
    border-color: #8b5cf6; /* Brighter border on hover */
}
/* Stop pulse animation on hover */
.kpi-item:hover {
    animation-play-state: paused;
}

/* KPI Labels */
.kpi-label {
    font-size: 1.3rem !important; /* Adjusted font size */
    color: #cbd5e0 !important; /* Light gray color */
    margin-bottom: 0.6rem; /* Adjusted margin */
    font-weight: 600; /* Semi-bold */
    text-align: center;
}

/* KPI Values */
.kpi-value {
    font-size: 2.8rem !important; /* Larger font size */
    font-weight: 800 !important; /* Extra bold */
    color: #ffffff !important;
    letter-spacing: -0.06em; /* Tighter spacing */
    text-align: center;
    word-wrap: break-word;
    text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.3); /* Subtle shadow */
}

/* Gradient Classes */
.gradient-blue-purple {
    background: linear-gradient(to right, #6366f1, #a855f7);
}
.gradient-purple-pink {
    background: linear-gradient(to right, #a855f7, #d946ef);
}
.gradient-pink-red {
    background: linear-gradient(to right, #d946ef, #f43f5e);
}
.gradient-red-orange {
    background: linear-gradient(to right, #f43f5e, #fb923c);
}

/* Logo Styling */
.logo {
    margin-bottom: 2.5rem; /* More space below logo */
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 180px; /* Slightly smaller logo */
    filter: drop-shadow(0 0 10px rgba(0, 188, 212, 0.5)); /* Add a subtle shadow to the logo */
    transition: transform 0.3s ease;
}
.logo:hover {
    transform: scale(1.1); /* Scale logo on hover */
}

/* Sidebar Styling */
.sidebar .sidebar-content {
    background-color: #2d3748; /* Darker background */
    padding: 2rem;
    border-radius: 15px;
    color: #ffffff;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    margin-top: 0;
    animation: fadeIn 1s ease;
}

/* Sidebar Headers */
.sidebar .sidebar-content h2 {
    color: #a78bfa; /* Lighter purple */
    border-bottom: 2px solid #a78bfa; /* Matching border */
    padding-bottom: 0.5rem;
    margin-top: 1rem; /* Adjusted top margin */
    margin-bottom: 1rem; /* Adjusted bottom margin */
}

/* Checkbox Styling */
.stCheckbox label {
    font-weight: 500;
    color: #ffffff;
    transition: color 0.2s ease;
}
.stCheckbox label:hover {
    color: #a78bfa; /* Highlight on hover */
}

/* Selectbox Styling */
select {
    background-color: #4a5568; /* Darker blue-gray */
    color: #fff;
    border: 1px solid #718096;
    padding: 0.9rem; /* Slightly more padding */
    border-radius: 0.6rem; /* Slightly more rounded */
    width: 100%;
    font-size: 1.1em;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.3s ease;
    cursor: pointer;
}
select:focus {
    outline: none;
    box-shadow: 0 0 0 4px rgba(167, 139, 250, 0.6); /* Stronger focus shadow */
    border-color: #a78bfa;
    background-color: #5a6375; /* Darker background on focus */
}

/* Plot Container (Streamlit's div wrapper) */
.stPlotlyChart {
    border: none;
    padding: 0; /* Remove padding */
    margin-bottom: 2.5rem; /* Add margin below plot */
    background-color: #1f1f1f; /* Match app background */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); /* Add shadow to plots */
    border-radius: 10px; /* Rounded corners for plot container */
    overflow: hidden; /* Hide overflow from border-radius */
    animation: fadeIn 1.5s ease; /* Fade in animation for plots */
}

/* DataFrame Styling */
.stDataFrame {
    border: 1px solid #4a5568; /* Darker border */
    border-radius: 10px; /* Rounded corners */
    padding: 1.5rem; /* Adjusted padding */
    background-color: #2d3748; /* Darker background */
    color: #ffffff;
    box_shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    animation: fadeIn 1.5s ease;
}

/* Specific styling for the Top Job Title container */
.top-job-title-container {
    background-color: #2d3748;
    padding: 2rem;
    border-radius: 15px;
    border: 2px solid #5a6375;
    text-align: center;
    margin_bottom: 3rem; /* More space below */
    animation: fadeIn 1s ease; /* Removed pulse from here */
    transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}
.top-job-title-container:hover {
    transform: translateY(-8px); /* Lift on hover */
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.6);
    background-color: #3a455a;
    border-color: #8b5cf6;
}
.top-job-title-label {
    font-size: 1.3rem !important;
    color: #cbd5e0 !important;
    margin_bottom: 0.6rem;
    font_weight: 600;
    text_align: center;
}
.top-job-title-value {
    font-size: 2.8rem !important;
    font_weight: 800 !important;
    color: #ffffff !important;
    letter_spacing: -0.06em;
    text_align: center;
    word_wrap: break_word;
    text_shadow: 1px 2px 4px rgba(0, 0, 0, 0.3);
    color: #00bcd4 !important; /* Highlight the value */
}

/* Summary Section Styling */
.summary-container {
    font_family: 'Inter', sans-serif; /* Use Inter font */
    background_color: #1f1f1f; /* Match app background */
    border_radius: 15px;
    padding: 30px; /* Increased padding */
    margin_top: 3rem; /* Added space above */
    margin_bottom: 20px;
    box_shadow: 0 8px 20px rgba(0, 0, 0, 0.3); /* Stronger shadow */
    width: 100%; /* Use full width */
    max_width: 1200px;
    margin_left: auto;
    margin_right: auto;
    color: #e0e0e0;
    display: flex;
    flex_direction: column;
    align_items: center;
    animation: fadeIn 1.5s ease;
    border: 1px solid #2d3748; /* Subtle border */
}
.summary-container h2 {
    color: #00bcd4; /* Cyan color */
    text_align: center;
    font_size: 2.8em; /* Increased font size */
    margin_bottom: 30px; /* More space below */
    font_weight: 800; /* Extra bold */
    display: flex;
    justify_content: center;
    align_items: center;
    border_bottom: 3px solid #00bcd4; /* Matching border */
    padding_bottom: 10px;
    width: 80%; /* Adjust width of the heading border */
}
.summary-container h2 i {
    margin_right: 15px;
    font_size: 1em; /* Relative size */
    color: #00bcd4;
}
.summary-point {
    background_color: #2d3748; /* Darker blue-gray */
    border_radius: 10px; /* More rounded */
    padding: 20px; /* Adjusted padding */
    margin: 15px 0; /* Adjusted margin */
    box_shadow: 0 3px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
    font_size: 1.15em; /* Slightly larger font size */
    color: #c0c0c0; /* Lighter gray text */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    width: 100%;
    max_width: 1100px; /* Adjust max_width for summary points */
    border_left: 5px solid #00bcd4; /* Highlight border on the left */
}
.summary-point:hover {
    transform: translateY(-5px);
    box_shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
    border_left_color: #a78bfa; /* Change highlight color on hover */
}
.highlight {
    color: #a78bfa; /* Lighter purple highlight */
    font_weight: 700; /* Bold highlight */
}
.summary-point ul {
    padding_left: 25px; /* More padding */
    list_style_type: disc;
    color: #e0e0e0; /* Match summary point text color */
}
.summary-point li {
    margin: 8px 0; /* More space between list items */
}
.summary-point h3 {
    color: #a78bfa; /* Lighter purple */
    font_size: 1.5em; /* Larger heading size */
    margin_bottom: 12px;
    font_weight: 700; /* Bold */
    border_bottom: none; /* Remove border below h3 in summary */
    padding_bottom: 0;
    margin_top: 0;
}

/* Responsiveness */
@media (max_width: 768px) {
    .stApp {
        padding: 1.5rem;
    }
    h1 {
        font_size: 3rem; /* Smaller title on mobile */
    }
    .kpi-container {
        flex_direction: column; /* Stack KPIs on mobile */
        align_items: center; /* Center stacked KPIs */
    }
    .kpi-item {
        min_width: 100%;
        margin_bottom: 1.5rem;
    }
    .sidebar {
        margin_top: 0;
    }
    .summary-container h2 {
        font_size: 2em; /* Smaller summary title on mobile */
    }
    .summary-point {
        font_size: 1em; /* Smaller summary text on mobile */
        padding: 15px;
    }
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        # Use the direct download link
        drive_url = "https://drive.google.com/uc?export=download&id=17jcNGGMozYXj-MJtYhqhpJqVATeOQGQ7"

        # Send a GET request to the Google Drive URL
        response = requests.get(drive_url)

        if response.status_code == 200:
            # Use StringIO to convert the response content into a file-like object for pandas to read
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)
            logging.info("Successfully loaded the CSV file from Google Drive")
            return df
        else:
            error_message = f"Failed to download the file from Google Drive, status code: {response.status_code}"
            st.error(error_message)
            logging.error(error_message)
            st.stop() # Stop execution if data loading fails

    except Exception as e:
        error_message = f"An error occurred while loading the CSV file: {e}"
        st.error(error_message)
        logging.exception(error_message)
        st.stop() # Stop execution if data loading fails

df = load_data()

# --- Title of the App ---
st.title("Job Market Demand Analysis")
st.markdown("""
This project aims to provide insights into the current job market by analyzing job postings data.
The goal is to help job seekers and employers understand market trends, including in-demand skills, job titles, and top companies.
""", unsafe_allow_html=True) # Using markdown for better formatting

# --- Add Logo ---
def get_base64_of_file(path):
    try:
        with open(path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded_image}"
    except FileNotFoundError:
        logging.error(f"Logo file not found at {path}")
        return None # Return None if file not found
    except Exception as e:
        logging.exception(f"Error loading logo file: {e}")
        return None

logo_path = "indeed_logo.png"
logo_base64 = get_base64_of_file(logo_path)

if logo_base64: # Only display if logo was loaded successfully
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img class="logo" src="{logo_base64}" alt="Company Logo">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Logo file not found. Please ensure 'indeed_logo.png' is in the correct directory.")


# --- Sidebar for Filters ---
st.sidebar.header("Filters")
all_categories = sorted(df['category'].unique())
# Set a default value that exists in the data, or 'All'
default_category = "IT" if "IT" in all_categories else all_categories[0] if all_categories else "All"
default_category_index = all_categories.index(default_category) + 1 if default_category != "All" and default_category in all_categories else 0 # +1 because of 'All' at the start
selected_category = st.sidebar.selectbox("Select Job Category", options=["All"] + all_categories, index=default_category_index)


# --- Location Filters ---
st.sidebar.header("Location Filters")
all_states = sorted(df['state'].unique())
selected_state = st.sidebar.selectbox("Select a State", options=["All"] + all_states)

# --- Data Filtering ---
def filter_data(df, selected_category, selected_state):
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df['state'] == selected_state]

    # Ensure relevant columns are string type and handle NaNs before plotting
    columns_to_process = ['category', 'job_title', 'company_name']
    for col in columns_to_process:
        if col in filtered_df.columns:
            # Convert to string, handling potential non-string NaNs first
            filtered_df[col] = filtered_df[col].astype(str).fillna('Unknown')

    # Process 'job_description' for skills, handle NaNs during extraction
    if 'job_description' in filtered_df.columns:
         filtered_df['job_description'] = filtered_df['job_description'].astype(str).fillna('') # Fill job_description NaNs with empty string for skill extraction

    # Process 'job_type', handle NaNs during categorization
    if 'job_type' in filtered_df.columns:
         filtered_df['job_type'] = filtered_df['job_type'].astype(str).fillna('') # Fill job_type NaNs with empty string for categorization


    return filtered_df

filtered_df = filter_data(df, selected_category, selected_state)

# --- Check if filtered data is empty ---
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    logging.info("Filtered dataframe is empty.")
    # Still show KPIs with default values or N/A
    total_postings = 0
    unique_categories = 0
    top_category = "N/A"
    top_title = "N/A"
    # Display KPIs with default values
    kpi_data = [
        {"label": "Total Job Postings", "value": f"{total_postings:,}", "color": "gradient-blue-purple"},
        {"label": "Unique Categories", "value": unique_categories, "color": "gradient-purple-pink"},
        {"label": "Top Job Category", "value": top_category, "color": "gradient-red-orange"},
    ]
    kpi_cols = st.columns(len(kpi_data))
    for i, kpi_col in enumerate(kpi_cols): # Iterate through columns directly
         # Create a container within each column for the KPI item HTML
         kpi_col.markdown(
            f"<div class='kpi-item {kpi_data[i]['color']}'><p class='kpi-label'>{kpi_data[i]['label']}</p><p class='kpi-value'>{kpi_data[i]['value']}</p></div>",
            unsafe_allow_html=True,
         )

    st.markdown(
        f"<div class='top-job-title-container'><p class='top-job-title-label'>Top Job Title</p><p class='top-job-title-value'>{top_title}</p></div>",
        unsafe_allow_html=True,
    )
    st.info("Try adjusting the filters to see data.")

else: # Proceed with displaying KPIs and plots if data is not empty
    # --- KPIs ---
    st.subheader("Key Performance Indicators")

    total_postings = len(filtered_df)
    unique_categories = filtered_df['category'].nunique()
    # Ensure value_counts index is not empty before accessing [0]
    top_category = filtered_df['category'].value_counts().index[0] if not filtered_df['category'].empty else "N/A"
    top_title = filtered_df['job_title'].value_counts().index[0] if not filtered_df['job_title'].empty else "N/A"

    kpi_data = [
        {"label": "Total Job Postings", "value": f"{total_postings:,}", "color": "gradient-blue-purple"},
        {"label": "Unique Categories", "value": unique_categories, "color": "gradient-purple-pink"},
        {"label": "Top Job Category", "value": top_category.upper() if top_category == "IT" else top_category, "color": "gradient-red-orange"},
    ]
    kpi_cols = st.columns(len(kpi_data))
    for i, kpi_col in enumerate(kpi_cols): # Iterate through columns directly
        kpi_col.markdown(
            f"<div class='kpi-item {kpi_data[i]['color']}'><p class='kpi-label'>{kpi_data[i]['label']}</p><p class='kpi-value'>{kpi_data[i]['value']}</p></div>",
            unsafe_allow_html=True,
        )

    # --- Top Job Title ---
    st.markdown(
        f"<div class='top-job-title-container'><p class='top-job-title-label'>Top Job Title</p><p class='top-job-title-value'>{top_title}</p></div>",
        unsafe_allow_html=True,
    )

    # --- Job Postings by Category ---
    st.subheader(f"Job Postings by Category in {selected_state if selected_state != 'All' else 'All States'}")
    # Use the processed 'category' column
    category_counts = filtered_df['category'].value_counts().head(15)
    if not category_counts.empty:
        fig_category_bar = px.bar(
            category_counts,
            x=category_counts.index,
            y=category_counts.values,
            # Labels defined here are for Plotly's internal use and hover
            labels={'x': 'Job Category', 'y': 'Number of Postings'},
            title="", # Title handled by subheader
            color_discrete_sequence=px.colors.sequential.Plasma,
            template="plotly_dark" # Apply dark theme
        )
        fig_category_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=22,
            font=dict(family='Inter', size=12),
            hoverlabel=dict(bgcolor="#2d3748", font_size=12, font_family="Inter"), # Darker hover label
            xaxis_title='Job Category', # Explicitly set x-axis title
            yaxis_title='Number of Postings' # Explicitly set y-axis title
        )
        st.plotly_chart(fig_category_bar, use_container_width=True)
    else:
        st.info("No category data available for the selected filters.")


    # --- Top Job Titles ---
    st.subheader(f"Top 10 Job Titles in {selected_state if selected_state != 'All' else 'All States'}")
    # Use the processed 'job_title' column
    job_title_counts = filtered_df['job_title'].value_counts().head(10)
    if not job_title_counts.empty:
        fig_job_title_bar = px.bar(
            job_title_counts,
            y=job_title_counts.index,
            x=job_title_counts.values,
            orientation='h',
            labels={'y': 'Job Title', 'x': 'Number of Postings'},
            title="", # Title handled by subheader
            color_discrete_sequence=px.colors.sequential.Viridis,
            template="plotly_dark" # Apply dark theme
        )
        fig_job_title_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=22,
            font=dict(family='Inter', size=12),
            hoverlabel=dict(bgcolor="#2d3748", font_size=12, font_family="Inter"), # Darker hover label
            yaxis_title='Job Title', # Explicitly set y-axis title
            xaxis_title='Number of Postings' # Explicitly set x-axis title
        )
        st.plotly_chart(fig_job_title_bar, use_container_width=True)
    else:
        st.info("No job title data available for the selected filters.")


    # --- Top Companies ---
    st.subheader(f"Top 10 Companies with Most Job Postings in {selected_state if selected_state != 'All' else 'All States'}")
    # Use the processed 'company_name' column
    company_counts = filtered_df['company_name'].value_counts().head(10)
    if not company_counts.empty:
        fig_company_bar = px.bar(
            company_counts,
            y=company_counts.index,
            x=company_counts.values,
            orientation='h',
            labels={'y': 'Company Name', 'x': 'Number of Postings'},
            title="", # Title handled by subheader
            color_discrete_sequence=px.colors.sequential.Teal,
            template="plotly_dark" # Apply dark theme
        )
        fig_company_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=22,
            font=dict(family='Inter', size=12),
            hoverlabel=dict(bgcolor="#2d3748", font_size=12, font_family="Inter"), # Darker hover label
            yaxis_title='Company Name', # Explicitly set y-axis title
            xaxis_title='Number of Postings' # Explicitly set x-axis title
        )
        st.plotly_chart(fig_company_bar, use_container_width=True)
    else:
        st.info("No company data available for the selected filters.")


    # --- Skills Demand Analysis ---
    st.subheader("Skills Demand Analysis")

    # Define a more comprehensive list of skills
    skill_keywords = [
        "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Swift", "Kotlin",
        "SQL", "NoSQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
        "AWS", "Azure", "GCP", "Cloud", "Docker", "Kubernetes", "Terraform", "Ansible",
        "React", "Angular", "Vue.js", "Node.js", "Spring", "Django", "Flask", "Ruby on Rails",
        "Data Analysis", "Machine Learning", "Deep Learning", "AI", "Data Science", "Big Data",
        "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy",
        "Communication", "Management", "Leadership", "Teamwork", "Problem Solving",
        "Agile", "Scrum", "Kanban", "Jira",
        "REST API", "GraphQL", "Microservices", "System Design",
        "Cybersecurity", "Networking", "DevOps", "CI/CD",
        "Salesforce", "SAP", "Oracle",
        "Financial Modeling", "Business Analysis", "Project Management",
        "Writing", "Editing", "Content Creation",
        "Marketing", "SEO", "SEM", "Social Media",
        "UI/UX Design", "Figma", "Sketch", "Adobe Creative Suite",
        "Customer Service", "Technical Support",
        "Budgeting", "Accounting", "Auditing",
        "Legal Research", "Compliance"
    ]
    # Ensure keywords are lowercased for case-insensitive matching
    skill_keywords_lower = [skill.lower() for skill in skill_keywords]

    def extract_skills(description, keywords_lower):
        if pd.isna(description): # Handle potential NaN values
            return []
        description_lower = str(description).lower() # Ensure it's a string
        found_skills = [skill for skill, keyword in zip(skill_keywords, keywords_lower) if keyword in description_lower]
        return found_skills

    try:
        # Apply skill extraction on the filtered data
        # Ensure 'job_description' is string type before applying
        if 'job_description' in filtered_df.columns:
            filtered_df['skills'] = filtered_df['job_description'].apply(lambda x: extract_skills(x, skill_keywords_lower))

            all_skills = [skill for sublist in filtered_df['skills'] for skill in sublist]
            skill_counts = Counter(all_skills)
            top_skills = skill_counts.most_common(15) # Show top 15 skills

            if top_skills:
                skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
                # Ensure 'Skill' column in skills_df is string type and handle potential NaNs (unlikely here but for robustness)
                skills_df['Skill'] = skills_df['Skill'].astype(str).fillna('Unknown Skill')

                fig_skills_bar = px.bar(
                    skills_df,
                    x='Count',
                    y='Skill',
                    orientation='h',
                    labels={'x': 'Number of Job Postings', 'y': 'Skill'},
                    title="", # Title handled by subheader
                    color_discrete_sequence=px.colors.sequential.Plasma,
                    template="plotly_dark" # Apply dark theme
                )
                fig_skills_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    title_font_size=22,
                    font=dict(family='Inter', size=12),
                     hoverlabel=dict(bgcolor="#2d3748", font_size=12, font_family="Inter"), # Darker hover label
                     xaxis_title='Number of Job Postings', # Explicitly set x-axis title
                     yaxis_title='Skill' # Explicitly set y-axis title
                )
                st.plotly_chart(fig_skills_bar, use_container_width=True)
            else:
                st.info("No skills found in the job descriptions for the selected filters.")
        else:
             st.warning("The 'job_description' column is not available in the dataset for skills analysis.")

    except KeyError:
        st.error("Error accessing 'job_description' column for skills extraction. Please check your data.")
        logging.error("KeyError: 'job_description' column missing during skill extraction.")
    except Exception as e:
        st.error(f"An unexpected error occurred while extracting skills: {e}")
        logging.exception(f"An unexpected error occurred during skill extraction: {e}")


    # --- Job Type Analysis ---
    st.subheader("Job Type Analysis")
    if 'job_type' in filtered_df.columns:
        # Ensure 'job_type' is not empty before proceeding
        # The fillna('') is done in filter_data now
        if not filtered_df['job_type'].empty: # Check if column exists and has data
            # Create a new column 'job_type_category'
            # Handle potential variations and map to Full-time/Part-time
            def categorize_job_type(job_type_str):
                if pd.isna(job_type_str) or job_type_str == '': # Handle NaN and empty string
                    return "Other/Unspecified"
                job_type_lower = str(job_type_str).lower() # Ensure it's a string before lowering
                if 'full-time' in job_type_lower or 'full time' in job_type_lower:
                    return 'Full-time'
                elif 'part-time' in job_type_lower or 'part time' in job_type_lower:
                    return 'Part-time'
                else:
                    # Catch any other non-matching string values here
                    return 'Other/Unspecified'

            # Apply categorization, ensure the output is string type
            filtered_df['job_type_category'] = filtered_df['job_type'].apply(categorize_job_type).astype(str)

            # Calculate the frequency of each job type category
            job_type_counts = filtered_df['job_type_category'].value_counts()

            if not job_type_counts.empty:
                # Create a pie chart to visualize the distribution
                fig_job_type_pie = px.pie(
                    job_type_counts,
                    names=job_type_counts.index,
                    values=job_type_counts.values,
                    title="", # Title handled by subheader
                    labels={'names': 'Job Type', 'values': 'Number of Postings'},
                    color_discrete_sequence=px.colors.sequential.Rainbow,
                    template="plotly_dark" # Apply dark theme
                )
                fig_job_type_pie.update_traces(
                    hoverinfo='label+percent+value',
                    textinfo='percent', # Only show percentage on the slice
                    marker=dict(line=dict(color='#1f1f1f', width=2)),
                    textposition='auto', # Let Plotly auto-position text
                    insidetextorientation='auto',
                    pull=[0.05] * len(job_type_counts) # Slightly pull slices for emphasis
                )
                fig_job_type_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    showlegend=True, # Show legend
                    title_font_size=22,
                    font=dict(family='Inter', size=12),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) # Position legend at the top
                )

                # Create two columns for the pie chart and the text
                col1, col2 = st.columns([1, 1])

                # Display the pie chart in the first column
                with col1:
                    st.plotly_chart(fig_job_type_pie, use_container_width=True)

                # Display the observations in the second column with improved styling
                with col2:
                    st.markdown("### Observations on Job Type")
                    # Using HTML/CSS for the observations list to match summary style
                    observations_html = "<div class='summary-point' style='border-left: none; box-shadow: none; background-color: #2d3748;'>"
                    observations_html += "<p>Based on the current filters:</p><ul>"
                    for job_type, count in job_type_counts.items():
                        percentage = (count / job_type_counts.sum()) * 100 if job_type_counts.sum() > 0 else 0
                        observations_html += f"<li><span class='highlight'>{job_type}:</span> {count:,} postings ({percentage:.2f}%)</li>"
                    observations_html += "</ul>"
                    observations_html += """
                    <p>Key takeaways from this distribution:</p>
                    <ul>
                        <li>The job market under the current filters is predominantly <span class="highlight">Full-time</span>.</li>
                        <li><span class="highlight">Part-time</span> and <span class="highlight">Other/Unspecified</span> roles make up a smaller portion.</li>
                        <li>This indicates a strong demand or preference for full-time employment in the analyzed segment.</li>
                    </ul>
                    </div>
                    """
                    st.markdown(observations_html, unsafe_allow_html=True)

            else:
                 st.info("No job type data available for the selected filters.")
        else:
             st.info("The 'job_type' column is present but contains no valid data for the selected filters.")
    else:
        st.markdown("<div class='plot-container'><p style='color:#ffaaaa;'>'job_type' column not found in the dataset.</p></div>", unsafe_allow_html=True)


# --- Summary Section ---
st.subheader("Job Market Insights Summary")

# Update the summary HTML to use the same styling classes and structure
# Font Awesome link is now outside this block
html_code = """
<div class="summary-container">
    <h2><i class="fas fa-briefcase"></i> Job Market Insights Summary</h2>
    <div class="summary-point">
        <h3>1. Overall Job Market Overview</h3>
        <p>The dataset provides a snapshot of the job market with <span class="highlight">{total_postings:,} job postings</span> (based on current filters). It covers <span class="highlight">{unique_categories:,} distinct job categories</span>, indicating its diverse nature.</p>
    </div>
    <div class="summary-point">
        <h3>2. Dominant Sector</h3>
        <p>The <span class="highlight">{top_category} sector</span> is the most prominent based on the highest number of job postings among the filtered data, highlighting its current strength.</p>
    </div>
    <div class="summary-point">
        <h3>3. Key Role in Demand</h3>
        <p>The role of <span class="highlight">{top_title}</span> is highly sought after, representing the job title with the most postings under the current selection. This suggests significant opportunities in this area.</p>
    </div>
"""

# Add company summary only if company_counts is available and not empty
# Ensure company_counts was calculated and is not empty
if 'company_counts' in locals() and not company_counts.empty:
    # Ensure we handle potential empty index gracefully
    if not company_counts.index.empty:
        top_companies_list = "</li><li>".join([f"<span class='highlight'>{company}</span>" for company in company_counts.index])
        html_code += f"""
        <div class="summary-point">
            <h3>4. Leading Employers</h3>
            <p>Based on the number of listings, key hiring companies include:</p>
            <ul>
                <li>{top_companies_list}</li>
            </ul>
            <p>These organizations are significant players in the current job market landscape.</p>
        </div>
        """

# Add skills summary only if top_skills is available and not empty
# Ensure top_skills was calculated and is not empty
if 'top_skills' in locals() and top_skills:
     # List top 5 skills if available
     num_skills_to_list = min(5, len(top_skills))
     if num_skills_to_list > 0:
        top_skills_list = ", ".join([f"<span class='highlight'>{skill[0]}</span>" for skill in top_skills[:num_skills_to_list]])
        html_code += f"""
        <div class="summary-point">
            <h3>5. Critical Skill Sets</h3>
            <p>Beyond specific roles, high-demand skills currently include {top_skills_list} and others, emphasizing the importance of both technical and transferable abilities.</p>
        </div>
        """

# Add job type summary only if job_type_counts is available and not empty
# Ensure job_type_counts was calculated and is not empty
if 'job_type_counts' in locals() and not job_type_counts.empty:
    full_time_percentage = job_type_counts.get('Full-time', 0) / job_type_counts.sum() * 100 if job_type_counts.sum() > 0 else 0
    html_code += f"""
    <div class="summary-point">
        <h3>6. Employment Type Trend</h3>
        <p>The majority of opportunities listed are <span class="highlight">full-time positions</span>, accounting for approximately <span class="highlight">{full_time_percentage:.2f}%</span> of postings under the current filters. This indicates a strong focus on permanent roles.</p>
    </div>
    """

html_code += """
    <div class="summary-point">
        <h3>7. Further Research Potential</h3>
        <p>This analysis serves as a foundation. Future exploration could involve examining <span class="highlight">salary data</span>, a more granular <span class="highlight">geographical breakdown</span>, and the <span class="highlight">evolution of skill demand</span> over time.</p>
    </div>
</div>
"""

# Format the HTML code with current KPI values
# Ensure variables used in format are defined even if filtered_df is empty
formatted_html = html_code.format(
    total_postings=total_postings,
    unique_categories=unique_categories,
    top_category=top_category if selected_category == "All" or top_category == "N/A" else f"the selected {selected_category} category ({top_category})",
    top_title=top_title
)
st.text("--- Raw HTML Content Below ---")
st.text(formatted_html)
st.text("--- End Raw HTML Content ---")
st.markdown(formatted_html, unsafe_allow_html=True)
