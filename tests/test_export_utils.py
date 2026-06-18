from __future__ import annotations

import json
from schemas import (
    CandidateEvaluation,
    KeywordMatchResult,
    ParsedDocument,
    ScoreBreakdown,
)
from export_utils import export_json, export_markdown


def test_export_json() -> None:
    eval_obj = CandidateEvaluation(
        file_name="test.pdf",
        candidate_name="Max",
        parsed_document=ParsedDocument(file_name="test.pdf", text="Max", page_count=1),
        keyword_match=KeywordMatchResult(),
        score=ScoreBreakdown(total_score=80.0, recommendation="High", explanation="Good"),
    )

    json_str = export_json([eval_obj])
    parsed_json = json.loads(json_str)

    assert isinstance(parsed_json, list)
    assert len(parsed_json) == 1
    assert parsed_json[0]["candidate_name"] == "Max"
    assert parsed_json[0]["score"]["total_score"] == 80.0


def test_export_markdown() -> None:
    eval_obj = CandidateEvaluation(
        file_name="test.pdf",
        candidate_name="Max",
        parsed_document=ParsedDocument(file_name="test.pdf", text="Max", page_count=1),
        keyword_match=KeywordMatchResult(),
        score=ScoreBreakdown(total_score=80.0, recommendation="High", explanation="Good"),
    )

    markdown_str = export_markdown([eval_obj])

    assert "# AI Resume Screening Ergebnis" in markdown_str
    assert "Rang 1: Max" in markdown_str
    assert "Gesamtscore: 80.0/100" in markdown_str
    assert "Datei: test.pdf" in markdown_str
