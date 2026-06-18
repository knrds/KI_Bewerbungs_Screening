from __future__ import annotations

import re

from config import DEFAULT_SCORE_WEIGHTS, ScoreWeights
from schemas import KeywordHit, KeywordMatchResult, ScoreBreakdown, ScoreComponent


def calculate_rule_based_score(
    match_result: KeywordMatchResult,
    resume_text: str = "",
    ai_fit_score: int | None = None,
    weights: ScoreWeights = DEFAULT_SCORE_WEIGHTS,
) -> ScoreBreakdown:
    must_points = _criteria_points(
        "Muss-Kriterien",
        match_result.must_have,
        weights.must_have,
    )
    nice_points = _criteria_points(
        "Wunsch-Kriterien",
        match_result.nice_to_have,
        weights.nice_to_have,
    )
    skill_points = _criteria_points(
        "Keyword-/Skill-Match",
        match_result.keywords,
        weights.skills,
    )
    seniority_points = _seniority_points(resume_text, weights.seniority)

    components = [must_points, nice_points, skill_points, seniority_points]
    raw_rule_score = sum(component.points for component in components)

    if ai_fit_score is None:
        if weights.total_without_ai <= 0:
            total_score = 0
        else:
            total_score = round((raw_rule_score / weights.total_without_ai) * 100, 1)
        explanation = (
            "Regelbasierter Score ohne KI-Anteil. "
            "Die verfuegbaren Regelpunkte wurden auf 100 skaliert."
        )
    else:
        ai_points_value = (_clamp(float(ai_fit_score), 0, 10) / 10) * weights.ai_semantic
        ai_points = ScoreComponent(
            name="KI-semantische Bewertung",
            points=round(ai_points_value, 1),
            max_points=weights.ai_semantic,
            explanation="Strukturierte KI-Einschaetzung, sofern verfuegbar.",
        )
        components.append(ai_points)
        total_score = round(sum(component.points for component in components), 1)
        explanation = "Regelbasierter Score plus optionale KI-Einschaetzung."

    total_score = _clamp(total_score, 0, 100)

    return ScoreBreakdown(
        total_score=total_score,
        components=components,
        recommendation=_recommendation(total_score),
        explanation=explanation,
    )


def _criteria_points(
    label: str,
    hits: list[KeywordHit],
    max_points: int,
) -> ScoreComponent:
    if not hits:
        return ScoreComponent(
            name=label,
            points=max_points,
            max_points=max_points,
            explanation=f"Keine {label} angegeben; Kategorie wird neutral bewertet.",
        )

    found_count = sum(1 for hit in hits if hit.found)
    ratio = found_count / len(hits)
    points = round(ratio * max_points, 1)
    return ScoreComponent(
        name=label,
        points=points,
        max_points=max_points,
        explanation=f"{found_count} von {len(hits)} Treffern gefunden.",
    )


def _seniority_points(resume_text: str, max_points: int) -> ScoreComponent:
    if not resume_text.strip():
        return ScoreComponent(
            name="Berufserfahrung / Senioritaet",
            points=0,
            max_points=max_points,
            explanation="Keine auswertbaren Textinformationen gefunden.",
        )

    normalized = resume_text.lower()
    years = _extract_years_of_experience(normalized)

    if any(term in normalized for term in ["senior", "lead", "principal", "head of"]):
        points = max_points
        explanation = "Senioritaetshinweise im Lebenslauf gefunden."
    elif years >= 5:
        points = max_points
        explanation = f"{years} Jahre Erfahrung erkannt."
    elif years >= 2:
        points = round(max_points * 0.6, 1)
        explanation = f"{years} Jahre Erfahrung erkannt."
    elif years >= 1:
        points = round(max_points * 0.3, 1)
        explanation = f"{years} Jahr(e) Erfahrung erkannt."
    else:
        points = round(max_points * 0.5, 1)
        explanation = "Senioritaet nicht eindeutig belegt; neutraler Zwischenwert."

    return ScoreComponent(
        name="Berufserfahrung / Senioritaet",
        points=points,
        max_points=max_points,
        explanation=explanation,
    )


def _extract_years_of_experience(text: str) -> int:
    matches = re.findall(
        r"(\d{1,2})\+?\s*(?:years|year|jahre|jahren)\s*(?:of)?\s*(?:experience|erfahrung|berufserfahrung)?",
        text,
    )
    if not matches:
        return 0
    return max(int(match) for match in matches)


def _recommendation(score: float) -> str:
    if score >= 80:
        return "Hohe Prioritaet fuer manuelle Pruefung"
    if score >= 65:
        return "Gute Prioritaet fuer manuelle Pruefung"
    if score >= 50:
        return "Manuell pruefen, mehrere offene Punkte"
    return "Niedrigere Prioritaet fuer manuelle Pruefung"


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))
