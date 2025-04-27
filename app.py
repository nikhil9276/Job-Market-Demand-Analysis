import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import logging
from io import StringIO
import base64
import requests
import os # Keep os import if needed elsewhere, though not used in provided snippet

# --- Constants ---
TOP_N_CATEGORIES = 15
TOP_N_TITLES = 10
TOP_N_COMPANIES = 10
TOP_N_SKILLS = 10
LOGO_PATH = "indeed_logo.png" # Make sure this path is correct relative to your script

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# --- Custom CSS for Enhanced Appearance ---
# Includes Font Awesome CDN
custom_css = """
<style>
    /* Import Font Awesome */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

    body {
        background-color: #121212; /* Dark background */
        color: #ffffff; /* White text */
        font-family: 'Inter', sans-serif; /* Modern font */
    }

    /* Main App Container Styling */
    .stApp {
        max-width: 1300px; /* Slightly wider */
        margin: 0 auto;
        padding: 2rem 2.5rem; /* Adjusted padding */
        background-color: #1f1f1f; /* Slightly lighter dark background */
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.7); /* Enhanced shadow */
        border-radius: 15px;
        color: #ffffff;
        display: flex;
        flex-direction: column;
    }

    /* --- Typography --- */

    /* Main Title (Gradient + Animation) */
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 5rem; /* Slightly smaller for balance */
        font-weight: bold;
        background: linear-gradient(to right, #6366f1, #8b5cf6, #d946ef);
        -webkit-background-clip: text;
        background-clip: text; /* Standard property */
        color: transparent;
        background-size: 300% 300%;
        line-height: 1.2;
        margin-bottom: 1.5rem; /* Reduced margin */
        letter-spacing: -0.02em;
        text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.6); /* Softer shadow */
        animation: gradientShift 4s ease-in-out infinite, textShadowPulse 2s ease-in-out infinite alternate;
    }

    /* Section Headings */
    h2, h3 {
        color: #a855f7; /* Purple accent */
        font-weight: bold;
        margin-top: 2.5rem; /* Consistent top margin */
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #a855f7; /* Slightly thinner line */
        padding-bottom: 0.5rem;
        animation: fadeIn 1s ease;
    }

    /* Sub Headings within sections */
    h4 {
        color: #cbd5e0; /* Lighter gray */
        font-weight: 500;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* --- Key Performance Indicators (KPIs) --- */
    .kpi-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 2.5rem;
        flex-wrap: wrap; /* Allow wrapping on smaller screens */
        gap: 1.5rem; /* Add gap between items */
    }

    .kpi-item {
        background-color: #2d3748; /* Darker gray-blue */
        padding: 1.75rem; /* Slightly reduced padding */
        border-radius: 12px; /* Softer radius */
        border: 1px solid #4a5568; /* Subtler border */
        text-align: center;
        flex-grow: 1; /* Allow items to grow */
        min-width: 200px; /* Minimum width */
        margin-bottom: 1rem; /* Space below if wrapped */
        animation: fadeIn 0.8s ease forwards, pulse 2.5s infinite alternate;
        transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    .kpi-item:hover {
        transform: translateY(-5px) scale(1.03); /* Lift and slightly enlarge */
        box-shadow: 0 10px 20px rgba(168, 85, 247, 0.4); /* Purple glow on hover */
        background-color: #4a5568;
        border-color: #a855f7;
    }

    .kpi-label {
        font-size: 1.1rem !important; /* Adjusted size */
        color: #cbd5e0 !important; /* Light gray */
        margin-bottom: 0.5rem; /* Reduced space */
        font-weight: 500;
    }

    .kpi-value {
        font-size: 2rem !important; /* Adjusted size */
        font-weight: bold !important;
        color: #ffffff !important;
        letter-spacing: -0.03em;
        word-wrap: break-word;
    }

    /* Top Job Title Specific Container */
    .top-job-title-container {
        background-color: #2d3748;
        padding: 1.75rem;
        border-radius: 12px;
        border: 1px solid #4a5568;
        text-align: center;
        margin: 1rem auto 2.5rem auto; /* Center and add margin */
        max-width: 500px; /* Control width */
        animation: fadeIn 1s ease, pulse 2.5s infinite alternate;
        transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    .top-job-title-container:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 10px 20px rgba(168, 85, 247, 0.4);
        background-color: #4a5568;
        border-color: #a855f7;
    }

    .top-job-title-label {
        font-size: 1.1rem !important;
        color: #cbd5e0 !important;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    .top-job-title-value {
        font-size: 2rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
        letter-spacing: -0.03em;
        word-wrap: break-word;
    }

    /* --- Sidebar Styling --- */
    .stSidebar > div:first-child { /* Target the sidebar itself */
       background-color: #2d3748;
       padding: 1.5rem;
       border-radius: 15px;
       margin-top: 1rem; /* Space from top */
       box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    .stSidebar .stSelectbox label {
        font-weight: 600;
        color: #a855f7; /* Match accent color */
        margin-bottom: 0.5rem;
    }

     .stSidebar .stSelectbox > div[data-baseweb="select"] > div { /* Target selectbox input */
        background-color: #4a5568;
        border: 1px solid #718096;
        border-radius: 0.5rem;
        color: #ffffff;
     }
     .stSidebar .stSelectbox > div[data-baseweb="select"] > div:focus-within { /* Focus state */
        border-color: #a78bfa;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.4);
     }

    /* --- Plotly Chart Container --- */
    .stPlotlyChart { /* Target Plotly containers */
      border-radius: 10px;
      padding: 1rem 0;
      margin-bottom: 2rem;
      background-color: #1f1f1f; /* Match app background */
      box-shadow: none; /* Remove default shadows if any */
      border: 1px solid #333; /* Subtle border */
    }

    /* --- DataFrame Styling --- */
    .stDataFrame {
        border: 1px solid #4a5568;
        border-radius: 10px;
        padding: 1rem;
        background-color: #2d3748; /* Consistent dark component background */
        color: #ffffff;
        margin-top: 1rem;
    }

    /* --- Logo Styling --- */
    .logo {
        margin-bottom: 1.5rem; /* Space below logo */
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 180px; /* Adjusted size */
        filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.4)); /* Add subtle shadow */
    }

    /* --- Summary Section Styling (Moved from HTML block) --- */
    .summary-container {
        font-family: 'Inter', sans-serif; /* Match main font */
        background-color: #2d3748; /* Consistent background */
        border-radius: 12px;
        padding: 2rem;
        margin: 2.5rem auto; /* Center and add vertical space */
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        width: 95%;
        max-width: 1100px; /* Control max width */
        color: #e0e0e0;
        border: 1px solid #4a5568;
    }

    .summary-container h2 { /* Styling the h2 inside summary */
        color: #a855f7; /* Accent color */
        text-align: center;
        font-size: 1.8em; /* Appropriate size */
        margin-bottom: 1.5rem;
        font-weight: bold;
        display: flex; /* For icon alignment */
        justify-content: center;
        align-items: center;
        border-bottom: none; /* Remove the default h2 border here */
    }

    .summary-container h2 i { /* Icon styling */
        margin-right: 12px;
        font-size: 1em; /* Match text size */
        color: #a855f7; /* Match heading color */
    }

     .summary-container h3 { /* Styling the h3 inside summary points */
        color: #00bcd4; /* Cyan highlight for point titles */
        font-size: 1.3em;
        margin-bottom: 0.8rem;
        font-weight: 600;
        border-bottom: none; /* Remove default h3 border */
        margin-top: 0; /* Reset margin */
     }

    .summary-point {
        background-color: #333; /* Darker background for contrast */
        border-radius: 8px;
        padding: 1rem 1.5rem; /* Adjusted padding */
        margin: 1rem 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        font-size: 1em; /* Standard text size */
        color: #e0e0e0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #00bcd4; /* Accent border */
    }

    .summary-point:hover {
        transform: translateX(5px); /* Slight shift on hover */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .highlight { /* Class for highlighting text */
        color: #00bcd4; /* Cyan highlight */
        font-weight: bold;
    }

    .summary-point ul {
        padding-left: 25px;
        list-style-type: disc;
        color: #f4f4f9;
        margin-top: 0.5rem;
    }

    .summary-point li {
        margin: 5px 0;
    }

    /* --- Gradient Background Classes for KPIs --- */
    .gradient-blue-purple { background: linear-gradient(to right, #6366f1, #a855f7); }
    .gradient-purple-pink { background: linear-gradient(to right, #a855f7, #d946ef); }
    .gradient-pink-red { background: linear-gradient(to right, #d946ef, #f43f5e); }
    .gradient-red-orange { background: linear-gradient(to right, #f43f5e, #fb923c); }

    /* --- Animations --- */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes textShadowPulse {
      from { text-shadow: 2px 3px 8px rgba(0, 0, 0, 0.4); }
      to { text-shadow: 3px 4px 12px rgba(0, 0, 0, 0.7); }
    }

    @keyframes pulse {
      from { transform: scale(0.98); }
      to { transform: scale(1); }
    }

    /* --- Responsive Design --- */
    @media (max-width: 768px) {
        .stApp {
            padding: 1rem 1.5rem;
        }
        h1 {
            font-size: 3.5rem; /* Smaller title on mobile */
        }
        .kpi-container {
            flex-direction: column; /* Stack KPIs vertically */
            align-items: stretch; /* Make items full width */
        }
        .kpi-item {
            min-width: unset; /* Remove min-width */
            width: 100%; /* Make full width */
            margin-bottom: 1rem;
        }
        .top-job-title-container {
            max-width: 90%;
        }
        .stSidebar { /* Adjust sidebar margin if needed */
            margin-top: 0;
        }
        .summary-container {
            width: 100%;
            padding: 1.5rem;
        }
        .summary-container h2 {
            font-size: 1.5em;
        }
         .summary-container h3 {
            font-size: 1.2em;
         }
         .summary-point {
             padding: 0.8rem 1rem;
         }
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads data from a Google Drive CSV link with error handling."""
    try:
        # Use the direct download link (ensure it remains valid)
        drive_url = "https://drive.google.com/uc?export=download&id=17jcNGGMozYXj-MJtYhqhpJqVATeOQGQ7"
        logging.info(f"Attempting to download data from: {drive_url}")

        response = requests.get(drive_url, timeout=30) # Added timeout
        response.raise_for_status() # Raises HTTPError for bad responses (4XX, 5XX)

        # Use StringIO to convert the response content into a file-like object
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        logging.info(f"Successfully loaded CSV. Shape: {df.shape}")

        # --- Basic Data Cleaning (Optional but Recommended) ---
        # Example: Convert relevant columns to string to avoid type errors later
        for col in ['category', 'state', 'job_title', 'company_name', 'job_description', 'job_type']:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna('Unknown') # Fill NA and ensure string type
        logging.info("Performed basic data cleaning (astype str, fillna).")

        return df

    except requests.exceptions.RequestException as e:
        error_message = f"Network error downloading file from Google Drive: {e}"
        st.error(error_message)
        logging.error(error_message)
        st.stop()
    except pd.errors.EmptyDataError:
        error_message = "The downloaded CSV file is empty."
        st.error(error_message)
        logging.error(error_message)
        st.stop()
    except Exception as e:
        error_message = f"An error occurred while loading or processing the CSV file: {e}"
        st.error(error_message)
        logging.exception(error_message) # Log full traceback
        st.stop()

df = load_data()

# --- Page Title ---
st.title("Job Market Demand Analysis")
st.markdown("""
Welcome! This dashboard provides insights into the job market using data scraped from job postings.
Explore trends in job categories, titles, companies, skills, and more. Use the filters in the sidebar to narrow down the analysis.
""") # Updated description


# --- Add Logo ---
def get_base64_of_file(path):
    """Reads a file and returns its base64 encoded string."""
    try:
        with open(path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded_image}"
    except FileNotFoundError:
        logging.warning(f"Logo file not found at: {path}. Skipping logo display.")
        return None
    except Exception as e:
        logging.error(f"Error reading logo file: {e}")
        return None

# IMPORTANT: Ensure 'indeed_logo.png' is in the same directory as your script,
# or provide the correct relative/absolute path.
logo_base64 = get_base64_of_file(LOGO_PATH)
if logo_base64:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img class="logo" src="{logo_base64}" alt="Indeed Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Sidebar for Filters ---
st.sidebar.header("Filters")

# Category Filter
all_categories = sorted(df['category'].unique())
# Try setting a default like 'IT' if it exists, otherwise default to 'All'
default_cat_index = 0
if "All" not in all_categories:
     all_categories_with_all = ["All"] + all_categories
else:
     all_categories_with_all = all_categories # If 'All' somehow exists

try:
    default_cat_index = all_categories_with_all.index("IT")
except ValueError:
    default_cat_index = 0 # Default to "All" if "IT" isn't found

selected_category = st.sidebar.selectbox(
    "Select Job Category",
    options=all_categories_with_all,
    index=default_cat_index # Set default index
)

# Location (State) Filter
all_states = sorted(df['state'].unique())
if "All" not in all_states:
     all_states_with_all = ["All"] + all_states
else:
    all_states_with_all = all_states

selected_state = st.sidebar.selectbox(
    "Select a State",
    options=all_states_with_all,
    index=0 # Default to "All"
)


# --- Data Filtering ---
def filter_data(dataf, category, state):
    """Filters the DataFrame based on selected category and state."""
    filtered_df = dataf.copy()
    if category != "All":
        filtered_df = filtered_df[filtered_df['category'] == category]
    if state != "All":
        filtered_df = filtered_df[filtered_df['state'] == state]
    logging.info(f"Data filtered. Category: {category}, State: {state}. Filtered rows: {len(filtered_df)}")
    return filtered_df

filtered_df = filter_data(df, selected_category, selected_state)

# --- Display Filtered Results Info ---
st.markdown(f"#### Showing results for: **{selected_category}** jobs in **{selected_state}**")

# --- Check if Filtered Data is Empty ---
if filtered_df.empty:
    st.warning("No job postings match the selected filters. Please broaden your search.")
    st.stop() # Stop execution if no data after filtering

# --- KPIs ---
st.header("Key Performance Indicators")

# Calculate KPIs safely after checking filtered_df is not empty
total_postings = len(filtered_df)
unique_categories = filtered_df['category'].nunique()
unique_titles_count = filtered_df['job_title'].nunique()

# Use value_counts() and handle potential empty series
top_category = filtered_df['category'].value_counts().index[0] if not filtered_df['category'].value_counts().empty else "N/A"
top_title = filtered_df['job_title'].value_counts().index[0] if not filtered_df['job_title'].value_counts().empty else "N/A"


kpi_data = [
    {"label": "Total Job Postings", "value": f"{total_postings:,}", "color": "gradient-blue-purple"},
    {"label": "Unique Job Titles", "value": f"{unique_titles_count:,}", "color": "gradient-purple-pink"}, # Changed KPI
    {"label": "Top Job Category", "value": top_category.upper() if top_category == "IT" else top_category, "color": "gradient-red-orange"},
]

# Display KPIs in columns
kpi_cols = st.columns(len(kpi_data))
for i, kpi in enumerate(kpi_data):
    with kpi_cols[i]:
        st.markdown(
            f"<div class='kpi-item {kpi['color']}'><p class='kpi-label'>{kpi['label']}</p><p class='kpi-value'>{kpi['value']}</p></div>",
            unsafe_allow_html=True,
        )

# --- Top Job Title (Separate Display) ---
st.markdown(
    f"<div class='top-job-title-container'><p class='top-job-title-label'>Top Job Title</p><p class='top-job-title-value'>{top_title}</p></div>",
    unsafe_allow_html=True,
)

# --- Common Plotly Layout ---
def get_plotly_layout():
    """Returns a dictionary for common Plotly layout settings."""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': '#ffffff',
        'title_font_size': 20, # Slightly smaller title
        'font': dict(family='Inter', size=12),
        'xaxis': dict(showgrid=False, zeroline=False), # Cleaner axes
        'yaxis': dict(showgrid=True, gridcolor='#444'), # Subtle gridlines on y-axis
        'legend': dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='#888'), # Semi-transparent legend
         'margin': dict(l=10, r=10, t=50, b=10) # Adjust margins
    }

# --- Job Postings by Category ---
st.header("Job Postings Distribution")

category_counts = filtered_df['category'].value_counts().head(TOP_N_CATEGORIES)
if not category_counts.empty:
    fig_category_bar = px.bar(
        category_counts,
        x=category_counts.index,
        y=category_counts.values,
        labels={'x': 'Job Category', 'y': 'Number of Postings'},
        title=f"Top {TOP_N_CATEGORIES} Job Categories ({'Filtered' if selected_category != 'All' or selected_state != 'All' else 'Overall'})", # Dynamic title part
        color_discrete_sequence=px.colors.sequential.Plasma_r, # Reversed Plasma
        template="plotly_dark" # Use plotly dark template base
    )
    fig_category_bar.update_layout(**get_plotly_layout()) # Apply common layout
    fig_category_bar.update_layout(xaxis_tickangle=-45) # Angle category names if long
    st.plotly_chart(fig_category_bar, use_container_width=True)
else:
    st.info("No category data to display for the current selection.")

# --- Top Job Titles ---
job_title_counts = filtered_df['job_title'].value_counts().head(TOP_N_TITLES)
if not job_title_counts.empty:
    fig_job_title_bar = px.bar(
        job_title_counts,
        y=job_title_counts.index,
        x=job_title_counts.values,
        orientation='h',
        labels={'y': 'Job Title', 'x': 'Number of Postings'},
        title=f"Top {TOP_N_TITLES} Job Titles ({selected_state if selected_state != 'All' else 'All States'})",
        color=job_title_counts.values, # Color by count
        color_continuous_scale=px.colors.sequential.Viridis, # Use Viridis scale
        template="plotly_dark"
    )
    fig_job_title_bar.update_layout(**get_plotly_layout())
    fig_job_title_bar.update_layout(yaxis={'categoryorder':'total ascending'}) # Order bars
    st.plotly_chart(fig_job_title_bar, use_container_width=True)
else:
    st.info("No job title data to display for the current selection.")


# --- Top Companies ---
st.header("Top Hiring Companies")
company_counts = filtered_df['company_name'].value_counts().head(TOP_N_COMPANIES)
if not company_counts.empty:
    fig_company_bar = px.bar(
        company_counts,
        y=company_counts.index,
        x=company_counts.values,
        orientation='h',
        labels={'y': 'Company Name', 'x': 'Number of Postings'},
        title=f"Top {TOP_N_COMPANIES} Companies ({selected_state if selected_state != 'All' else 'All States'})",
        color=company_counts.values,
        color_continuous_scale=px.colors.sequential.Tealgrn, # Changed color sequence
        template="plotly_dark"
    )
    fig_company_bar.update_layout(**get_plotly_layout())
    fig_company_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_company_bar, use_container_width=True)
else:
    st.info("No company data to display for the current selection.")


# # --- Skills Demand Analysis ---
# st.header("Skills in Demand")

# # Define skills list (consider making this configurable or loading from a file)
# SKILLS_LIST = [
#     "Python", "JavaScript", "Java", "C++", "C#", "SQL", "NoSQL", "AWS", "Azure", "GCP",
#     "Docker", "Kubernetes", "Terraform", "React", "Angular", "Vue", "Node.js",
#     "Data Analysis", "Machine Learning", "Deep Learning", "AI", "Statistics", "Pandas", "NumPy", "Scikit-learn",
#     "Communication", "Leadership", "Management", "Project Management", "Agile", "Scrum"
# ]

# def extract_skills(description):
#     """Extracts predefined skills from a job description (case-insensitive)."""
#     if not isinstance(description, str):
#         return []
#     # Use word boundaries (\b) to avoid matching substrings (e.g., 'java' in 'javascript')
#     found_skills = [skill for skill in SKILLS_LIST if pd.Series(description.lower()).str.contains(fr'\b{skill.lower()}\b', regex=True).any()]
#     return found_skills

# # Check if 'job_description' column exists
# if 'job_description' in filtered_df.columns:
#     try:
#         # Apply skill extraction to the FILTERED dataframe
#         filtered_df['skills'] = filtered_df['job_description'].apply(extract_skills)
#         logging.info("Skill extraction completed.")

#         # Flatten the list of skills
#         all_skills = [skill for sublist in filtered_df['skills'] for skill in sublist]

#         if all_skills:
#             skill_counts = Counter(all_skills)
#             top_skills = skill_counts.most_common(TOP_N_SKILLS)

#             skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])

#             fig_skills_bar = px.bar(
#                 skills_df,
#                 x='Count',
#                 y='Skill',
#                 orientation='h',
#                 labels={'Count': 'Frequency in Postings', 'Skill': 'Skill'},
#                 title=f"Top {TOP_N_SKILLS} Skills Mentioned ({'Filtered' if selected_category != 'All' or selected_state != 'All' else 'Overall'})",
#                 color='Count',
#                 color_continuous_scale=px.colors.sequential.Magenta, # Different color scale
#                 template="plotly_dark"
#             )
#             fig_skills_bar.update_layout(**get_plotly_layout())
#             fig_skills_bar.update_layout(yaxis={'categoryorder':'total ascending'})
#             st.plotly_chart(fig_skills_bar, use_container_width=True)
#         else:
#             st.info("No predefined skills found in the job descriptions for the current selection.")

#     except Exception as e:
#         st.error(f"An error occurred during skills analysis: {e}")
#         logging.exception("Error during skills analysis")
# else:
#     st.warning("The 'job_description' column is missing. Cannot perform skills analysis.")
#     logging.warning("'job_description' column not found for skills analysis.")


# --- Job Type Analysis ---
st.header("Job Type Distribution")

if 'job_type' in filtered_df.columns:
    # Simplified job type categorization
    def categorize_job_type(jt):
        jt_lower = str(jt).lower()
        if 'full-time' in jt_lower or 'full time' in jt_lower:
            return 'Full-time'
        elif 'part-time' in jt_lower or 'part time' in jt_lower:
            return 'Part-time'
        elif 'contract' in jt_lower:
            return 'Contract'
        elif 'internship' in jt_lower:
            return 'Internship'
        elif 'temporary' in jt_lower:
            return 'Temporary'
        else:
            return 'Other/Unspecified' # Catch-all

    filtered_df['job_type_category'] = filtered_df['job_type'].apply(categorize_job_type)

    job_type_counts = filtered_df['job_type_category'].value_counts()

    if not job_type_counts.empty:
        fig_job_type_pie = px.pie(
            job_type_counts,
            names=job_type_counts.index,
            values=job_type_counts.values,
            title=f"Job Type Distribution ({selected_state if selected_state != 'All' else 'All States'})",
            hole=0.3, # Make it a donut chart
            color_discrete_sequence=px.colors.sequential.RdBu, # Changed color sequence
            template="plotly_dark"
        )
        fig_job_type_pie.update_traces(
            textposition='outside',
            textinfo='percent+label',
            pull=[0.05 if i == 0 else 0 for i in range(len(job_type_counts))], # Pull the largest slice
            marker=dict(line=dict(color='#1f1f1f', width=2))
        )
        fig_job_type_pie.update_layout(**get_plotly_layout())
        fig_job_type_pie.update_layout(showlegend=False, title_font_size=20) # Hide legend for pie

        # Display chart and metrics side-by-side
        col1, col2 = st.columns([2, 1]) # Chart takes more space

        with col1:
            st.plotly_chart(fig_job_type_pie, use_container_width=True)

        with col2:
            st.markdown("#### Breakdown:")
            total = job_type_counts.sum()
            for job_type, count in job_type_counts.items():
                percentage = (count / total) * 100 if total > 0 else 0
                st.metric(label=job_type, value=f"{count:,}", delta=f"{percentage:.1f}%")
            # Add a note about the categorization
            st.caption("Note: Job types are broadly categorized (Full-time, Part-time, Contract, etc.). 'Other' includes unspecified or less common types.")

    else:
        st.info("No job type data to display for the current selection.")
else:
    st.warning("'job_type' column not found. Cannot perform job type analysis.")
    logging.warning("'job_type' column not found for job type analysis.")


# --- Display the raw data (optional) ---
st.header("Explore Raw Data")
if st.checkbox("Show Filtered Raw Data Sample"):
    st.markdown("Displaying a sample of the filtered job postings data.")
    st.dataframe(filtered_df.head(50)) # Show top 50 rows of filtered data
    st.caption(f"Total filtered postings: {len(filtered_df):,}")

# --- Summary Section (Using the HTML block) ---
st.header("Overall Summary & Insights")

# Note: This summary is static based on the original analysis.
# For a dynamic summary reflecting filters, you'd need to recalculate these points based on filtered_df.
html_code = """
<div class="summary-container">
    <h2><i class="fas fa-briefcase"></i> Initial Dataset Insights Summary</h2>
    <div class="summary-point">
        <h3>1. Overall Job Market Overview</h3>
        <p>The initial dataset comprised <span class="highlight">~29,500+ job postings</span> across numerous distinct job categories, indicating a diverse job market landscape at the time of data collection.</p>
    </div>
    <div class="summary-point">
        <h3>2. Dominant Sector</h3>
        <p>The <span class="highlight">IT sector</span> showed significant activity in the original data, often having the highest number of job postings.</p>
    </div>
    <div class="summary-point">
        <h3>3. Key Role</h3>
        <p>Roles like <span class="highlight">"Software Developer"</span> frequently appeared among the most in-demand titles, highlighting a consistent need for software development skills.</p>
    </div>
    <div class="summary-point">
        <h3>4. Leading Employers</h3>
        <p>Major corporations like <span class="highlight">JPMorgan Chase Bank, N.A.</span>, <span class="highlight">IBM</span>, and <span class="highlight">Accenture</span> were often listed among the top hiring companies in the initial dataset.</p>
    </div>
    <div class="summary-point">
        <h3>5. Critical Skill Sets</h3>
        <p>Alongside technical skills (like Python, Java, Cloud platforms), <span class="highlight">Management</span> and <span class="highlight">Communication</span> were frequently sought after, emphasizing the value of soft skills.</p>
    </div>
    <div class="summary-point">
        <h3>6. Employment Type Trend</h3>
        <p>The job market analyzed was heavily dominated by <span class="highlight">full-time positions</span>, typically representing over 90% of postings.</p>
    </div>
    <div class="summary-point">
        <h3>7. Further Research Potential</h3>
        <p>Further analysis could explore <span class="highlight">salary trends</span>, deeper <span class="highlight">geographical distributions</span> (city-level), and the evolution of skill demands over time.</p>
    </div>
    <p style="text-align: center; margin-top: 20px; font-size: 0.9em; color: #ccc;"><i>Note: This summary reflects insights from the initial, unfiltered dataset. Use the filters and interactive charts above for current, specific analysis.</i></p>
</div>
"""
st.markdown(html_code, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.caption("Dashboard developed using Streamlit & Plotly | Data Source: Scraped Job Postings (Illustrative)")
