from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel

from schemas import CandidateEvaluation


def export_json(data: Any) -> str:
    return json.dumps(_to_serializable(data), indent=2, ensure_ascii=False)


def export_markdown(evaluations: list[CandidateEvaluation]) -> str:
    lines = [
        "# AI Resume Screening Ergebnis",
        "",
        f"Exportiert am: {datetime.now(UTC).isoformat()}",
        "",
        "Hinweis: Dieses Ergebnis ist eine Entscheidungshilfe und keine finale HR-Entscheidung.",
        "",
    ]

    for index, evaluation in enumerate(evaluations, start=1):
        lines.extend(
            [
                f"## Rang {index}: {evaluation.candidate_name}",
                "",
                f"- Datei: {evaluation.file_name}",
                f"- Gesamtscore: {evaluation.score.total_score}/100",
                f"- Empfehlung: {evaluation.score.recommendation}",
                f"- Fehlende Muss-Kriterien: {', '.join(evaluation.keyword_match.missing_must_have) or 'keine'}",
                "",
            ]
        )

        if evaluation.ai_analysis:
            lines.extend(
                [
                    "### KI-Kurzprofil",
                    "",
                    evaluation.ai_analysis.candidate_summary or "Nicht verfuegbar.",
                    "",
                ]
            )

    return "\n".join(lines)


def _to_serializable(data: Any) -> Any:
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json")

    if isinstance(data, list):
        return [_to_serializable(item) for item in data]

    if isinstance(data, dict):
        return {key: _to_serializable(value) for key, value in data.items()}

    return data
