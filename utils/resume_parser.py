from docx import Document
import pdfplumber

def extract_resume_text(file_path):
    """Extract text from a resume file (DOCX or PDF)."""
    if file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a DOCX or PDF file.")
    
def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    except Exception as e:
        raise ValueError(f"Error reading DOCX file: {e}")

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = []
            for page in pdf.pages:
                text.append(page.extract_text())
            return '\n'.join(text)
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")