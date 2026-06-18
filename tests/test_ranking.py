from __future__ import annotations

from schemas import (
    CandidateEvaluation,
    KeywordMatchResult,
    ParsedDocument,
    ScoreBreakdown,
)
from ranking import sort_candidates, build_ranking_table


def _make_dummy_evaluation(name: str, score: float) -> CandidateEvaluation:
    return CandidateEvaluation(
        file_name=f"{name.lower()}.pdf",
        candidate_name=name,
        parsed_document=ParsedDocument(file_name=f"{name.lower()}.pdf", text="", page_count=1),
        keyword_match=KeywordMatchResult(),
        score=ScoreBreakdown(total_score=score, recommendation="Test", explanation="Test"),
    )


def test_sort_candidates() -> None:
    cand_a = _make_dummy_evaluation("Candidate A", 50.0)
    cand_b = _make_dummy_evaluation("Candidate B", 90.0)
    cand_c = _make_dummy_evaluation("Candidate C", 75.0)

    sorted_list = sort_candidates([cand_a, cand_b, cand_c])

    assert sorted_list[0].candidate_name == "Candidate B"
    assert sorted_list[1].candidate_name == "Candidate C"
    assert sorted_list[2].candidate_name == "Candidate A"


def test_build_ranking_table() -> None:
    cand_a = _make_dummy_evaluation("Candidate A", 50.0)
    cand_b = _make_dummy_evaluation("Candidate B", 90.0)

    df = build_ranking_table([cand_a, cand_b])

    assert len(df) == 2
    assert list(df.columns) == [
        "Rang",
        "Bewerber",
        "Datei",
        "Gesamtscore",
        "Muss-Kriterien erfuellt",
        "Wunsch-Kriterien erfuellt",
        "Keyword-Matches",
        "KI-Score",
        "Kurzprofil",
        "Offene Punkte",
        "Empfehlung",
    ]
    assert df.loc[0, "Bewerber"] == "Candidate B"
    assert df.loc[0, "Rang"] == 1
    assert df.loc[1, "Bewerber"] == "Candidate A"
    assert df.loc[1, "Rang"] == 2
