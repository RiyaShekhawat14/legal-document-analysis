import os
import shutil
import uuid
from pathlib import Path
import PyPDF2
from fastapi import UploadFile
from config.settings import settings
from utils.logger import logger

try:
    import pdfplumber
except ImportError:
    pdfplumber = None
    logger.warning("pdfplumber is not installed. PDF extraction will use PyPDF2 only.")

UPLOAD_DIR = settings.UPLOAD_DIR


def _safe_filename(filename: str) -> str:
    base = Path(filename).name
    name, ext = os.path.splitext(base)
    safe_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    return safe_name


def save_uploaded_file(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    safe_name = _safe_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def extract_text_from_file(file: UploadFile) -> str:
    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith(".txt"):
        content = file.file.read()
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1", errors="replace")

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

    # If PyPDF2 failed, try pdfplumber when available
    if not text and pdfplumber is not None:
        try:
            file.file.seek(0)
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception:
            pass

    return text
