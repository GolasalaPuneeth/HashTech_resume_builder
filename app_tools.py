import os
import shutil
import fitz
import docx
import uuid
from fastapi import HTTPException

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    return text

async def extract_text_from_word(docx_path):
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Word document not found: {docx_path}") 
    text = ""
    try:
        doc = docx.Document(docx_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        raise Exception(f"Error extracting text from Word document: {str(e)}")
    return text

async def text_extracter(filePath: str)-> str:
    file_extension = os.path.splitext(filePath)[1].lower()
    if file_extension == ".pdf":
        return await extract_text_from_pdf(filePath)
    elif file_extension in [".docx", ".doc"]:
        return await extract_text_from_word(filePath)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

async def save_file(resume):
    file_extension = os.path.splitext(resume.filename)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        # Close the file
        resume.file.close()
        return file_path