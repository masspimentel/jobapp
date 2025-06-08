import streamlit as st
from utils.resume_parser import extract_resume_text
from utils.jsearch_api import find_jobs as search_jobs
from utils.gpt_utils import generate_cover_letter, extract_job_search_keywords
from utils.drive import upload_to_drive
from utils.sheets import log_to_sheets
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Job Application Bot", page_icon=":briefcase:", layout="centered")
st.title("Job Application Bot :briefcase:")

st.button("Location", key="location_button", help="Click to set your location for job search")
location = st.text_input("Enter your location (optional)", placeholder="e.g., Toronto, Canada")
st.write("This app helps you find jobs based on your resume and a job description, and generates a cover letter for you.")

job_title = st.text_input("Enter the job title you are looking for (optional)", placeholder="e.g., Software Engineer")

resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Enter the job description")

if st.button("Find jobs and generate cover letter"):
    if not resume_file or not job_description:
        st.error("Please upload a resume and enter a job description.")
    else:
        extension = resume_file.name.split('.')[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp:
            temp.write(resume_file.read())
            temp_path = temp.name
        
        st.info("Extracting text from resume...")
        resume_text = extract_resume_text(temp_path)

        st.success("Resume text extracted successfully.")

        st.info("Generating job search keywords from resume...")

        if job_title:
            resume_summary = extract_job_search_keywords(resume_text, job_title)
        else:
            resume_summary = extract_job_search_keywords(resume_text, job_description)
            
        st.info("Searching for jobs...")

        # Add before line 50:
        st.write("Searching with query:", resume_summary[:100] + "..." if len(resume_summary) > 100 else resume_summary)
        try:
            jobs = search_jobs(resume_summary, location=location)
            st.write(f"API response: {jobs if not isinstance(jobs, list) else 'Received job list'}")
        except Exception as e:
            st.error(f"Error searching for jobs: {e}")
            jobs = []

        if not jobs:
            st.error("No jobs found for the given resume and job description.")
        else:
            st.success(f"Found {len(jobs)} jobs.")
            for job in jobs:
                job_posting = f"**{job['title']}** at {job['company']}\nLocation: {job['location']}\nLink: [View Job]({job['link']})"
                st.markdown(job_posting)

            selected_job = st.selectbox("Select a job to generate a cover letter", [job['title'] for job in jobs])
            if st.button("Generate Cover Letter"):
                selected_job_details = next(job for job in jobs if job['title'] == selected_job)
                cover_letter = generate_cover_letter(resume_text, selected_job_details['description'])

                if cover_letter:
                    st.success("Cover letter generated successfully.")
                    st.text_area("Cover Letter", value=cover_letter, height=300)

                    if st.button("Upload to Google Drive"):
                        drive_link = upload_to_drive(cover_letter, selected_job['title'])
                        st.success(f"Cover letter uploaded to Google Drive: {drive_link}")

                    if st.button("Log to Google Sheets"):
                        log_to_sheets(selected_job_details, cover_letter)
                        st.success("Job and cover letter logged to Google Sheets.")
                else:
                    st.error("Failed to generate cover letter.")
        os.remove(temp_path)
        
        
        
