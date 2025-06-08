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
    
def extract_job_search_keywords(resume_text, job_title=None):
    """Extract specific keywords from resume for job search queries."""
    try:
        prompt = "Extract 3-5 key skills and job titles from this resume that would be most effective for job searching. Return ONLY keywords separated by spaces, no commas or other punctuation."
        if job_title:
            prompt += f" Focus on skills relevant to {job_title} positions."
            
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts relevant job search keywords from resumes."},
                {"role": "user", "content": f"{prompt}\n\nResume:\n{resume_text}"}
            ],
            max_tokens=50,  # Shorter to keep it focused
            temperature=0.3
        )
        keywords = response.choices[0].message.content.strip()
        return keywords
    except Exception as e:
        st.error(f"GPT Error: {e}")
        print(f"An error occurred while extracting resume keywords: {e}")
        return None