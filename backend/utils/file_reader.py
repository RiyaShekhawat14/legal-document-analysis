import os
import shutil
import PyPDF2
import pdfplumber
from fastapi import UploadFile

UPLOAD_DIR = "uploads"


def save_uploaded_file(file: UploadFile) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith(".txt"):
        content = file.file.read()
        return content.decode("utf-8")

    else:
        return ""


def extract_text_from_pdf(file: UploadFile) -> str:
    text = ""

    # Try PyPDF2 first
    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except:
        pass

    # If PyPDF2 failed, try pdfplumber
    if not text:
        try:
            file.file.seek(0)
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except:
            pass

    return text