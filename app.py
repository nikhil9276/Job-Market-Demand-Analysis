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

# Custom CSS for enhanced appearance
custom_css = """
<style>
body {
    background-color: #121212;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}
.stApp {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2.5rem;
    background-color: #1f1f1f;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.7);
    border-radius: 15px;
    color: #ffffff;
    display: flex;
    flex-direction: column;
}
h1 {
    color: #ffffff;
    text-align: center;
    font-size: 6rem;
    font-weight: bold;
    background: linear-gradient(to right, #6366f1, #8b5cf6, #d946ef);
    -webkit-background-clip: text;
    color: transparent;
    background-size: 300% 300%;
    line-height: 1.2;
    margin-bottom: 2rem;
    letter-spacing: -0.02em;
    text-shadow: 2px 4px 6px rgba(0, 0, 0, 0.5);
    animation: gradientShift 3s ease-in-out infinite, textShadow 1s ease-in-out infinite;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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
h2, h3, h4 {
    color: #a855f7;
    animation: fadeIn 1s ease;
    font-weight: bold;
    margin-top: 3rem;
    margin-bottom: 1.5rem;
    border-bottom: 4px solid #a855f7; /* Added line below heading */
    padding-bottom: 0.5rem;
}
.kpi-container {
    display: flex;
    justify-content: space-around;
    margin-bottom: 2.5rem;
    flex-wrap: wrap;
}
.kpi-item {
    background-color: #2d3748;
    padding: 2.25rem;
    border-radius: 15px;
    border: 2px solid #6b7280;
    text-align: center;
    min-width: 220px;
    margin-bottom: 1.75rem;
    animation: fadeIn 1s ease, pulse 2s infinite alternate;
    transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.3s ease;
    display: flex; /* Add flexbox to the kpi-item */
    flex-direction: column; /* Stack label and value vertically */
    justify-content: center; /* Vertically center content */
    align-items: center; /* Horizontally center content */
}
.kpi-item:hover {
    transform: scale(1.06);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.5);
    background-color: #4a5568;
    border-color: #a78bfa;
}
@keyframes pulse {
  from { transform: scale(0.94); }
  to { transform: scale(1); }
}
.kpi-label {
    font-size: 1.4rem !important;
    color: #cbd5e0 !important;
    margin-bottom: 0.75rem;
    font-weight: 500;
    text-align: center; /* Center the label */
}
.kpi-value {
    font-size: 2.5rem !important;
    font-weight: bold !important;
    color: #ffffff !important;
    letter-spacing: -0.05em;
    text-align: center; /* Center the value */
    word-wrap: break-word; /* Wrap long words */
}
.sidebar .sidebar-content {
    background-color: #2d3748;
    padding: 2rem;
    border-radius: 15px;
    color: #ffffff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    margin-top: 0;
}
.stCheckbox label {
    font-weight: 500;
    color: #ffffff;
}
select {
    background-color: #4a5568;
    color: #fff;
    border: 1px solid #718096;
    padding: 0.8rem;
    border-radius: 0.5rem;
    width: 100%;
    font-size: 1.1rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.3s ease;
}
select:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.5);
    border-color: #a78bfa;
    background-color: #6b7280;
}
.plot-container {
  border: none;
  padding: 1rem 0;
  margin-bottom: 2rem;
  background-color: #1f1f1f;
  box-shadow: none;
}
.stDataFrame {
    border: 1px solid #6b7280;
    border-radius: 15px;
    padding: 1.25rem;
    background-color: #1f1f1f;
    color: #ffffff;
}
/* New styles for gradients and animations */
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
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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
h1 {
    color: #ffffff;
    text-align: center;
    font-size: 6rem;
    font-weight: bold;
    background: linear-gradient(to right, #6366f1, #8b5cf6, #d946ef);
    -webkit-background-clip: text;
    color: transparent;
    background-size: 300% 300%;
    line-height: 1.2;
    margin-bottom: 2rem;
    letter-spacing: -0.02em;
    text-shadow: 2px 4px 6px rgba(0, 0, 0, 0.5);
    animation: gradientShift 3s ease-in-out infinite, textShadow 1s ease-in-out infinite;
}
.logo {
    margin-bottom: 1rem;
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 200px;
}
.sidebar {
    margin-top: 5rem;
}
.sidebar .sidebar-content {
    background-color: #2d3748;
    padding: 2rem;
    border-radius: 15px;
    color: #ffffff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}
.top-job-title-container {
    background-color: #2d3748;
    padding: 2.25rem;
    border-radius: 15px;
    border: 2px solid #6b7280;
    text-align: center;
    margin-bottom: 1.75rem;
    animation: fadeIn 1s ease, pulse 2s infinite alternate;
    transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.3s ease;
}
.top-job-title-container:hover {
    transform: scale(1.06);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.5);
    background-color: #4a5568;
    border-color: #a78bfa;
}
.top-job-title-label {
    font-size: 1.4rem !important;
    color: #cbd5e0 !important;
    margin-bottom: 0.75rem;
    font-weight: 500;
    text-align: center;
}
.top-job-title-value {
    font-size: 2.5rem !important;
    font-weight: bold !important;
    color: #ffffff !important;
    letter-spacing: -0.05em;
    text-align: center;
    word-wrap: break-word;
}
@media (max-width: 768px) {
    .stApp {
        padding: 1.5rem;
    }
    .kpi-item {
        min-width: 100%;
        margin-bottom: 1.5rem;
    }
    .sidebar {
        margin-top: 0;
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
            st.stop()

    except Exception as e:
        error_message = f"An error occurred while loading the CSV file: {e}"
        st.error(error_message)
        logging.exception(error_message)
        st.stop()

df = load_data()

# --- Title of the App ---
st.title("Job Market Demand Analysis")
st.markdown("This project aims to provide insights into the current job market by analyzing job postings data.  The goal is to help job seekers and employers understand market trends, including in-demand skills, job titles, and top companies.", unsafe_allow_html=True)

# --- Add Logo ---
def get_base64_of_file(path):
    with open(path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

logo_path =  "indeed_logo.png"  # Make sure this is the correct relative path to your logo
logo_base64 = get_base64_of_file(logo_path)
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img class="logo" src="{logo_base64}">
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sidebar for Filters ---
st.sidebar.header("Filters")
all_categories = sorted(df['category'].unique())
selected_category = st.sidebar.selectbox("Select Job Category", options=["All"] + all_categories, index=all_categories.index("IT") if "IT" in all_categories else 0)

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
    return filtered_df

filtered_df = filter_data(df, selected_category, selected_state)

# --- KPIs ---
st.subheader("Key Performance Indicators")

total_postings = len(filtered_df)
unique_categories = filtered_df['category'].nunique()
unique_titles = f"{filtered_df['job_title'].nunique():,}"
top_category = filtered_df['category'].value_counts().index[0] if not filtered_df.empty else "N/A"
top_title = filtered_df['job_title'].value_counts().index[0] if not filtered_df.empty else "N/A"

kpi_data = [
    {"label": "Total Job Postings", "value": f"{total_postings:,}", "color": "gradient-blue-purple"},
    {"label": "Unique Categories", "value": unique_categories, "color": "gradient-purple-pink"},
    {"label": "Top Job Category", "value": top_category.upper() if top_category == "IT" else top_category, "color": "gradient-red-orange"},
]

kpi_cols = st.columns(len(kpi_data))

for i, kpi in enumerate(kpi_data):
    with kpi_cols[i]:
        st.markdown(
            f"<div class='kpi-item {kpi['color']}'><p class='kpi-label'>{kpi['label']}</p><p class='kpi-value'>{kpi['value']}</p></div>",
            unsafe_allow_html=True,
        )

# --- Top Job Title ---
st.markdown(
    f"<div class='top-job-title-container'><p class='top-job-title-label'>Top Job Title</p><p class='top-job-title-value'>{top_title}</p></div>",
    unsafe_allow_html=True,
)

# --- Job Postings by Category ---
category_counts = filtered_df['category'].value_counts().head(15)  # Show top 15 categories
fig_category_bar = px.bar(
    category_counts,
    x=category_counts.index,
    y=category_counts.values,
    labels={'x': 'Job Category', 'y': 'Number of Postings'},
    title=f"Job Postings by Category in {selected_state if selected_state != 'All' else 'All States'}", # Don't change the title
    color_discrete_sequence=px.colors.sequential.Plasma,
)
fig_category_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#ffffff',
    title_font_size=22,
    font=dict(family='Inter', size=12),
)
st.plotly_chart(fig_category_bar)


# --- Top Job Titles ---
job_title_counts = filtered_df['job_title'].value_counts().head(10) # Change to top 10
fig_job_title_bar = px.bar(
    job_title_counts,
    y=job_title_counts.index,
    x=job_title_counts.values,
    orientation='h',
    labels={'y': 'Job Title', 'x': 'Number of Postings'},
    title=f"Top 10 Job Titles in {selected_state if selected_state != 'All' else 'All States'}", # Change to top 10
    color_discrete_sequence=px.colors.sequential.Viridis, # Change color sequence
)
fig_job_title_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#ffffff',
    title_font_size=22,
    font=dict(family='Inter', size=12),
)
st.plotly_chart(fig_job_title_bar)

# --- Top Companies ---
st.subheader("Top Companies")
company_counts = filtered_df['company_name'].value_counts().head(10)
fig_company_bar = px.bar(
    company_counts,
    y=company_counts.index,
    x=company_counts.values,
    orientation='h',
    labels={'y': 'Company Name', 'x': 'Number of Postings'},
    title=f"Top 10 Companies with Most Job Postings in {selected_state if selected_state != 'All' else 'All States'}",
    color_discrete_sequence=px.colors.sequential.Teal, # Change color sequence to Teal
)
fig_company_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#ffffff',
    title_font_size=22,
    font=dict(family='Inter', size=12),
)
st.plotly_chart(fig_company_bar)


# # --- Skills Demand Analysis ---
# st.subheader("Skills Demand Analysis") # Changed the title here - Removed duplicate

# def extract_skills(description):
#     skills = ["Python", "JavaScript", "Java", "C++", "SQL", "AWS", "Azure", "Docker", "Kubernetes", "React",
#               "Angular", "Node.js", "Data Analysis", "Machine Learning", "Communication", "Management"]
#     found_skills = [skill for skill in skills if skill.lower() in description.lower()]
#     return found_skills

# try:
#     df['skills'] = df['job_description'].apply(extract_skills) # Use the original DataFrame here
# except KeyError as e:
#         st.error(f"Error: The 'job_description' column is missing. Please check your data.  KeyError: {e}")
#         logging.error(f"KeyError: {e}.  The 'job_description' column is missing.")
#         st.stop()
# except Exception as e:
#         st.error(f"An unexpected error occurred while extracting skills: {e}")
#         logging.exception(f"An unexpected error occurred: {e}")
#         st.stop()

# all_skills = [skill for sublist in df['skills'] for skill in sublist] # Use the original DataFrame here
# skill_counts = Counter(all_skills)
# top_skills = skill_counts.most_common(10)

# if top_skills:
#     skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
#     fig_skills_bar = px.bar(
#         skills_df,
#         x='Count',
#         y='Skill',
#         orientation='h',
#         labels={'x': 'Number of Job Postings', 'y': 'Skill'}, # Changed x-axis label to 'Number of Job Postings'
#         title=f"Top 10 Skills in Demand", # Removed the state filter
#         color_discrete_sequence=px.colors.sequential.Plasma
#     )
#     fig_skills_bar.update_layout(
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         font_color='#ffffff',
#         title_font_size=22,
#         font=dict(family='Inter', size=12),
#     )
#     st.plotly_chart(fig_skills_bar)
# else:
#     st.markdown(
#         "<div class='plot-container'><p style='color:#ffaaaa;'>No skills found in the job descriptions.</p></div>",
#         unsafe_allow_html=True)

# --- Job Type Analysis ---
st.subheader("Job Type Analysis") # Moved this line up
if 'job_type' in filtered_df.columns:
    # Create a new column 'job_type_category'
    filtered_df['job_type_category'] = filtered_df['job_type'].apply(lambda x: 'Full-time' if 'Full-time' in x else 'Part-time')

    # Calculate the frequency of each job type category
    job_type_counts = filtered_df['job_type_category'].value_counts()

    # Create a pie chart to visualize the distribution
    fig_job_type_pie = px.pie(
        job_type_counts,
        names=job_type_counts.index,
        values=job_type_counts.values,
        title=f"Job Type Distribution in {selected_state if selected_state != 'All' else 'All States'}", # shortened title
        labels={'names': 'Job Type Category', 'values': 'Number of Postings'},
        color_discrete_sequence=px.colors.sequential.Rainbow, # Changed color sequence
    )
    fig_job_type_pie.update_traces(
        hoverinfo='label+percent+value',
        textinfo='label+percent+value',
        marker=dict(line=dict(color='#1f1f1f', width=2)),
        # Display labels and values outside the pie chart
        textposition='outside',
        insidetextorientation='auto'
    )
    fig_job_type_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        showlegend=False,
        title_font_size=22,
        font=dict(family='Inter', size=12),
    )
    # Create two columns for the pie chart and the text
    col1, col2 = st.columns([1, 1])  # Adjust the ratio as needed

    # Display the pie chart in the first column
    with col1:
        st.plotly_chart(fig_job_type_pie)

    # Display the observations in the second column
    with col2:
        st.write("Observations:")
        st.write("-   Full-time jobs are dominant, accounting for approximately 96.44% of the total job postings.")
        st.write("-   Part-time jobs represent a smaller portion, accounting for about 3.56% of the total postings.")
        st.write("-   The high percentage of Full-time positions suggests a strong preference or demand for full-time employment in this market.")


else:
    st.markdown("<div class='plot-container'><p style='color:#ffaaaa;'>'job_type' column not found.</p></div>", unsafe_allow_html=True)

# --- Display the raw data (optional) ---
# if st.checkbox("Show Raw Data"): # Removed the checkbox
#     st.subheader("Raw Data (Filtered)")
#     st.dataframe(filtered_df)


html_code = """
<style>
    .summary-container {
        font-family: Arial, sans-serif;
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 25px;
        margin: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        width: 95%;  /* Increased width */
        margin: 0 auto;
        color: #e0e0e0;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .summary-container h2 {
        color: #f4f4f9;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 25px;
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .summary-container h2 i {
        margin-right: 15px;
        font-size: 2.5em;
        color: #00bcd4;
    }
    .summary-point {
        background-color: #333;
        border-radius: 8px;
        padding: 18px;
        margin: 12px 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        font-size: 1.1em;
        color: #e0e0e0;
        transition: transform 0.3s;
        width: 100%;  /* Ensures it stretches to fill the container */
        max-width: 1200px;  /* Increase the max-width to make it even wider */
    }
    .summary-point:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .highlight {
        color: #00bcd4;
        font-weight: bold;
    }
    .summary-point ul {
        padding-left: 20px;
        list-style-type: disc;
        color: #f4f4f9;
    }
    .summary-point li {
        margin: 5px 0;
    }
    .summary-point h3 {
        color: #00bcd4;
        font-size: 1.4em;
        margin-bottom: 10px;
    }
</style>

<div class="summary-container">
    <h2><i class="fas fa-briefcase"></i> Job Market Insights Summary</h2>
    <div class="summary-point">
        <h3>1. Overall Job Market Overview</h3>
        <p>The dataset comprises <span class="highlight">29,575 job postings</span> spanning <span class="highlight">63 distinct job categories</span>, indicating a diverse job market.</p>
    </div>
    <div class="summary-point">
        <h3>2. Dominant Sector</h3>
        <p>The <span class="highlight">IT sector</span> emerges as the most active, evidenced by the highest number of job postings and the identification of <span class="highlight">"IT"</span> as the top job category.</p>
    </div>
    <div class="summary-point">
        <h3>3. Key Role</h3>
        <p>The role of <span class="highlight">"Software Developer"</span> is in significant demand, holding the highest number of postings among all job titles. This highlights a strong need for software development professionals.</p>
    </div>
    <div class="summary-point">
        <h3>4. Leading Employers</h3>
        <p>The top companies with the highest volume of job listings are:</p>
        <ul>
            <li><span class="highlight">JPMorgan Chase Bank, N.A.</span></li>
            <li><span class="highlight">IBM</span></li>
            <li><span class="highlight">Accenture</span></li>
        </ul>
        <p>This suggests these are major hiring entities within this analyzed market.</p>
    </div>
    <div class="summary-point">
        <h3>5. Critical Skill Sets</h3>
        <p>Beyond technical expertise, <span class="highlight">Management</span> and <span class="highlight">Communication skills</span> are highly sought after across various roles, indicating the importance of both hard and soft skills in the job market.</p>
    </div>
    <div class="summary-point">
        <h3>6. Employment Type Trend</h3>
        <p>The job market is heavily skewed towards <span class="highlight">full-time positions</span>, representing approximately <span class="highlight">96.44%</span> of all postings, indicating a strong preference for full-time employment opportunities.</p>
    </div>
    <div class="summary-point">
        <h3>7. IT Sector Demand</h3>
        <p>The initial data suggests a <span class="highlight">robust IT sector</span> with a high demand for software developers. This reflects the rapid growth and expansion of the tech industry.</p>
    </div>
    <div class="summary-point">
        <h3>8. Key Soft Skills</h3>
        <p>Strong <span class="highlight">Management</span> and <span class="highlight">Communication skills</span> are valuable assets for job seekers across all job categories.</p>
    </div>
    <div class="summary-point">
        <h3>9. Full-Time Opportunities</h3>
        <p>The predominant offering in the market is <span class="highlight">full-time roles</span>, which suggests job stability and long-term career growth for applicants.</p>
    </div>
    <div class="summary-point">
        <h3>10. Further Research Potential</h3>
        <p>Further analysis could delve into <span class="highlight">salary trends</span>, <span class="highlight">geographical distribution</span> of roles, and the <span class="highlight">correlation between skills</span> and job titles.</p>
    </div>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)
