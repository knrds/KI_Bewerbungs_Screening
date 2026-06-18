from __future__ import annotations

import pandas as pd

from schemas import CandidateEvaluation


def sort_candidates(
    evaluations: list[CandidateEvaluation],
) -> list[CandidateEvaluation]:
    return sorted(
        evaluations,
        key=lambda evaluation: evaluation.score.total_score,
        reverse=True,
    )


def build_ranking_table(evaluations: list[CandidateEvaluation]) -> pd.DataFrame:
    rows = []
    for rank, evaluation in enumerate(sort_candidates(evaluations), start=1):
        match = evaluation.keyword_match
        ai = evaluation.ai_analysis

        rows.append(
            {
                "Rang": rank,
                "Bewerber": evaluation.candidate_name,
                "Datei": evaluation.file_name,
                "Gesamtscore": evaluation.score.total_score,
                "Muss-Kriterien erfuellt": _format_hit_ratio(match.must_have),
                "Wunsch-Kriterien erfuellt": _format_hit_ratio(match.nice_to_have),
                "Keyword-Matches": _format_hit_ratio(match.keywords),
                "KI-Score": ai.ai_fit_score if ai else None,
                "Kurzprofil": ai.candidate_summary if ai else "",
                "Offene Punkte": "; ".join(match.missing_must_have),
                "Empfehlung": evaluation.score.recommendation,
            }
        )

    return pd.DataFrame(rows)


def _format_hit_ratio(hits) -> str:
    if not hits:
        return "nicht angegeben"

    found = sum(1 for hit in hits if hit.found)
    return f"{found}/{len(hits)}"
