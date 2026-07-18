import os
from pathlib import Path
from typing import BinaryIO, Optional

import pdfplumber
from docx import Document


def load_text_from_file(uploaded_file: BinaryIO) -> str:
    """Extract plain text from uploaded PDF, DOCX, or TXT files."""
    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix == ".txt":
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if suffix == ".pdf":
        return extract_text_from_pdf(uploaded_file)

    if suffix == ".docx":
        return extract_text_from_docx(uploaded_file)

    raise ValueError(f"Unsupported file type: {suffix}")


def extract_text_from_pdf(uploaded_file: BinaryIO) -> str:
    """Extract text from a PDF using pdfplumber."""
    text_chunks: list[str] = []
    uploaded_file.seek(0)

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text() or ""
            text_chunks.append(extracted_text)

    return "\n".join(text_chunks)


def extract_text_from_docx(uploaded_file: BinaryIO) -> str:
    """Extract text from a DOCX document using python-docx."""
    uploaded_file.seek(0)
    document = Document(uploaded_file)
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)
