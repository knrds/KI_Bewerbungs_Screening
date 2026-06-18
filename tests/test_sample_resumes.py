from __future__ import annotations

from pathlib import Path

from keyword_matcher import match_candidate_text
from pdf_parser import extract_text_from_pdf


SAMPLE_RESUME_DIR = Path("sample_data/fake_resumes")

EXPECTED_SAMPLE_FILES = [
    "max_mustermann.pdf",
    "erika_musterfrau.pdf",
    "john_doe.pdf",
    "lea_synonym_match.pdf",
    "otto_manager_profile.pdf",
    "nina_data_analyst.pdf",
    "scan_ohne_text.pdf",
]


def test_demo_resume_files_exist() -> None:
    missing = [
        file_name
        for file_name in EXPECTED_SAMPLE_FILES
        if not (SAMPLE_RESUME_DIR / file_name).exists()
    ]
    assert missing == []


def test_demo_resume_pdfs_are_parseable() -> None:
    for file_name in EXPECTED_SAMPLE_FILES:
        parsed = extract_text_from_pdf(SAMPLE_RESUME_DIR / file_name)

        assert parsed.page_count >= 1
        if file_name == "scan_ohne_text.pdf":
            assert parsed.is_empty is True
            assert parsed.text == ""
        else:
            assert parsed.is_empty is False
            assert len(parsed.text) > 120


def test_synonym_sample_matches_job_requirements() -> None:
    parsed = extract_text_from_pdf(SAMPLE_RESUME_DIR / "lea_synonym_match.pdf")

    result = match_candidate_text(
        text=parsed.text,
        must_have="Python, SQL, REST API",
        nice_to_have="Docker, React, AWS",
        keywords="Git, Kommunikation",
    )

    assert all(hit.found for hit in result.must_have)
    assert all(hit.found for hit in result.nice_to_have)
    assert result.missing_must_have == []
