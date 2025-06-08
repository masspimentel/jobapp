import openai
import os
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI(api_key=api_key)

def generate_cover_letter(resume_text, job_description):
    """Generate a cover letter using OpenAI's GPT-4o model."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant that generates professional cover letters."},
                {"role": "user", "content": f"Generate a cover letter based on the following resume and job description:\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        cover_letter = response.choices[0].message.content.strip()
        return cover_letter
    except Exception as e:
        st.error(f"GPT Error: {e}")
        print(f"An error occurred while generating the cover letter: {e}")
        return None
    
def summarize_resume_for_search(resume_text):
    """Summarize the resume text for job search."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes resumes for job search purposes."},
                {"role": "user", "content": f"Summarize this resume into a concise summary that highlights key skills and experiences:\n\n{resume_text}"}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        st.error(f"GPT Error: {e}")
        print(f"An error occurred while summarizing the resume: {e}")
        return None