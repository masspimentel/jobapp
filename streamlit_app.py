import streamlit as st
from utils.resume_parser import extract_resume_text
from utils.jsearch_api import find_jobs as search_jobs
from utils.gpt_utils import generate_cover_letter, extract_job_search_keywords
from utils.drive import upload_to_drive
from utils.sheets import log_to_sheets
import tempfile
import os
import pandas as pd

# Initialize session state to hold variables across reruns
if 'jobs_df' not in st.session_state:
    st.session_state.jobs_df = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'cover_letter' not in st.session_state:
    st.session_state.cover_letter = ""
if 'selected_job_title' not in st.session_state:
    st.session_state.selected_job_title = ""


st.set_page_config(page_title="Job Application Bot", page_icon=":briefcase:", layout="centered")
st.title("Job Application Bot :briefcase:")

st.info("This app helps you find jobs, generate a tailored cover letter, and track your applications.")

# --- Step 1: Inputs ---
st.header("1. Enter Your Details")
location = st.text_input("Enter your location (e.g., Toronto, Canada)", key="location_input")
job_title = st.text_input("Enter the target job title (e.g., Software Engineer)", key="job_title_input")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("For a targeted search, paste a sample job description here")


# --- Step 2: Find Jobs ---
st.header("2. Find a Job")
if st.button("Find Jobs", key="find_jobs_button"):
    if not resume_file:
        st.error("Please upload a resume to find jobs.")
    else:
        # Reset previous results
        st.session_state.jobs_df = None
        st.session_state.cover_letter = ""
        st.session_state.selected_job_title = ""
        
        with st.spinner("Analyzing your resume and searching for jobs..."):
            extension = resume_file.name.split('.')[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp:
                temp.write(resume_file.read())
                temp_path = temp.name
            
            # Store resume text in session state
            st.session_state.resume_text = extract_resume_text(temp_path)
            os.remove(temp_path)

            if st.session_state.resume_text:
                st.success("Successfully extracted text from your resume.")

                search_query_base = job_title if job_title else job_description
                if not search_query_base:
                    st.warning("No job title or description provided; search may be broad.")
                
                search_keywords = extract_job_search_keywords(st.session_state.resume_text, search_query_base)
                st.info(f"Searching for jobs with keywords: '{search_keywords}'")

                try:
                    jobs_list = search_jobs(search_keywords, location=location)
                    if jobs_list:
                        st.session_state.jobs_df = pd.DataFrame(jobs_list)
                        st.success(f"Found {len(st.session_state.jobs_df)} jobs!")
                    else:
                        st.error("No jobs found. Try adjusting your job title or description.")
                except Exception as e:
                    st.error(f"An error occurred while searching for jobs: {e}")
            else:
                st.error("Could not extract text from the resume.")

# --- Step 3: Generate Cover Letter ---
if st.session_state.jobs_df is not None and not st.session_state.jobs_df.empty:
    st.header("3. Select a Job and Generate Cover Letter")

    # Clean up job titles for display
    jobs = st.session_state.jobs_df.to_dict('records')
    job_titles = [f"{job.get('job_title', 'N/A')} at {job.get('employer_name', 'N/A')}" for job in jobs]

    selected_job_display_title = st.selectbox(
        "Select a job to generate a cover letter for:",
        options=job_titles,
        index=0,
        key="job_selection"
    )

    if st.button("Generate Cover Letter", key="generate_cl_button"):
        with st.spinner("Generating your cover letter..."):
            # Find the full details of the selected job
            selected_job_index = job_titles.index(selected_job_display_title)
            selected_job_details = jobs[selected_job_index]
            
            # Get the full job description, which might be under different keys
            full_job_desc = selected_job_details.get('job_description') or "No description provided."

            # Generate and store the cover letter
            cover_letter = generate_cover_letter(st.session_state.resume_text, full_job_desc)
            if cover_letter:
                st.session_state.cover_letter = cover_letter
                st.session_state.selected_job_title = selected_job_display_title
                st.success("Cover letter generated successfully!")
            else:
                st.error("Failed to generate the cover letter. Please try again.")

# --- Step 4: Review and Use Cover Letter ---
if st.session_state.cover_letter:
    st.header(f"4. Your Cover Letter for {st.session_state.selected_job_title}")
    
    st.text_area("Generated Cover Letter", st.session_state.cover_letter, height=400)
    
    # Logic for uploads can be added here, for example:
    st.markdown("---")
    st.write("What would you like to do next?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload to Google Drive", key="upload_drive_button"):
            # This part requires you to handle how the file is saved locally before upload
            # For now, let's assume `upload_to_drive` can handle text content directly
            # Note: Your `upload_to_drive` function expects a file_path, so we need to save it first
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt", encoding="utf-8") as temp:
                temp.write(st.session_state.cover_letter)
                temp_path = temp.name

            try:
                # Find selected job details again
                jobs = st.session_state.jobs_df.to_dict('records')
                job_titles = [f"{job.get('job_title', 'N/A')} at {job.get('employer_name', 'N/A')}" for job in jobs]
                selected_job_index = job_titles.index(st.session_state.selected_job_title)
                selected_job_details = jobs[selected_job_index]
                
                file_name = f"Cover Letter - {selected_job_details.get('job_title', 'Job')}.txt"
                drive_id = upload_to_drive(temp_path, file_name)
                st.success(f"Cover letter uploaded to Google Drive with ID: {drive_id}")
            except Exception as e:
                st.error(f"Failed to upload to Google Drive: {e}")
            finally:
                os.remove(temp_path)


    with col2:
        if st.button("Log to Google Sheets", key="log_sheets_button"):
            # You would need to implement the logging logic based on your sheet's structure
            # Example: log_to_sheets(selected_job_details, st.session_state.cover_letter)
            st.info("Logging to Google Sheets... (functionality to be fully implemented)")