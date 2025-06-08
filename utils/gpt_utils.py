import openai
import os
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI(api_key=api_key)

def generate_cover_letter(resume_text, job_description):
    """Generate a cover letter using OpenAI's GPT-3.5 model."""
    try:
        response = client.responses.create(
            model="gpt-4o",
            prompt=f"Generate a cover letter based on the following resume and job description:\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nCover Letter:",
            max_tokens=500,
            temperature=0.7
        )
        cover_letter = response.choices[0].text.strip()
        return cover_letter
    except Exception as e:
        st.error(f"GPT Error: {e}")
        print(f"An error occurred while generating the cover letter: {e}")
        return None
    
def summarize_resume_for_search(resume_text):
    """Summarize the resume text for job search."""
    try:
        response = client.responses.create(
            model="gpt-4o",
            prompt=f"Summarize the following resume for job search:\n\n{resume_text}\n\nSummary:",
            max_tokens=200,
            temperature=0.5
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        st.error(f"GPT Error: {e}")
        print(f"An error occurred while summarizing the resume: {e}")
        return None