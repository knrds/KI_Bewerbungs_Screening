from __future__ import annotations

import io
import pytest
import fitz
from pdf_parser import clean_text, extract_text_from_pdf, PDFParsingError


def test_clean_text() -> None:
    raw_text = "Hello\x00World \t  with\n\n  multiple   spaces  "
    cleaned = clean_text(raw_text)
    assert cleaned == "Hello World with\nmultiple spaces"


def test_extract_text_from_valid_pdf() -> None:
    # Generate a simple PDF in-memory
    doc = fitz.open()
    page = doc.new_page()
    page.insert_textbox(fitz.Rect(50, 50, 500, 500), "Hello Python Developer\nExperience: 5 years.")
    pdf_bytes = doc.write()
    doc.close()

    result = extract_text_from_pdf(pdf_bytes, file_name="test_resume.pdf")

    assert result.file_name == "test_resume.pdf"
    assert "Hello Python Developer" in result.text
    assert "Experience: 5 years." in result.text
    assert result.page_count == 1
    assert result.is_empty is False
    assert len(result.warnings) == 0


def test_extract_text_from_empty_pdf() -> None:
    doc = fitz.open()
    doc.new_page()  # Empty page
    pdf_bytes = doc.write()
    doc.close()

    result = extract_text_from_pdf(pdf_bytes, file_name="empty.pdf")
    assert result.is_empty is True
    assert "No readable text found" in result.warnings[0]


def test_extract_text_invalid_source() -> None:
    with pytest.raises(PDFParsingError):
        extract_text_from_pdf(b"invalid pdf content header")
