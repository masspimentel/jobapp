import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(resume_text, job_description):
    """Generate a cover letter using OpenAI's GPT-3.5 model."""
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"Generate a cover letter based on the following resume and job description:\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nCover Letter:",
            max_tokens=500,
            temperature=0.7
        )
        cover_letter = response.choices[0].text.strip()
        return cover_letter
    except Exception as e:
        print(f"An error occurred while generating the cover letter: {e}")
        return None