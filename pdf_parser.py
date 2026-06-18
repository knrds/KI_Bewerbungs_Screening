from __future__ import annotations

import re
from pathlib import Path
from typing import BinaryIO

import fitz

from schemas import ParsedDocument


class PDFParsingError(RuntimeError):
    pass


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_text_from_pdf(
    source: str | Path | bytes | BinaryIO,
    file_name: str | None = None,
) -> ParsedDocument:
    document = None

    try:
        if isinstance(source, (str, Path)):
            path = Path(source)
            document = fitz.open(path)
            resolved_file_name = file_name or path.name
        else:
            pdf_bytes = _read_bytes(source)
            document = fitz.open(stream=pdf_bytes, filetype="pdf")
            resolved_file_name = file_name or getattr(source, "name", "uploaded_resume.pdf")

        page_texts = []
        for page in document:
            page_text = clean_text(page.get_text("text") or "")
            if page_text:
                page_texts.append(page_text)

        extracted_text = clean_text("\n\n".join(page_texts))
        warnings = []
        if not extracted_text:
            warnings.append("No readable text found. The PDF may be scanned or empty.")

        return ParsedDocument(
            file_name=resolved_file_name,
            text=extracted_text,
            page_count=document.page_count,
            is_empty=not bool(extracted_text),
            warnings=warnings,
        )
    except Exception as exc:
        raise PDFParsingError(f"Could not parse PDF: {exc}") from exc
    finally:
        if document is not None:
            document.close()


def _read_bytes(source: bytes | BinaryIO) -> bytes:
    if isinstance(source, bytes):
        return source

    if hasattr(source, "getvalue"):
        return source.getvalue()

    if hasattr(source, "seek"):
        source.seek(0)

    data = source.read()

    if hasattr(source, "seek"):
        source.seek(0)

    return data
