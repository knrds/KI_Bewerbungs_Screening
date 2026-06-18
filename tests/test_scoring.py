from __future__ import annotations

from config import ScoreWeights
from schemas import KeywordHit, KeywordMatchResult
from scoring import (
    calculate_rule_based_score,
    _extract_years_of_experience,
    _recommendation,
)


def test_extract_years_of_experience() -> None:
    assert _extract_years_of_experience("i have 5 years of experience in python") == 5
    assert _extract_years_of_experience("10+ jahre berufserfahrung") == 10
    assert _extract_years_of_experience("keine angabe") == 0
    assert _extract_years_of_experience("3 year experience, 1 year of java") == 3


def test_recommendation_tiers() -> None:
    assert _recommendation(85) == "Hohe Prioritaet fuer manuelle Pruefung"
    assert _recommendation(72) == "Gute Prioritaet fuer manuelle Pruefung"
    assert _recommendation(55) == "Manuell pruefen, mehrere offene Punkte"
    assert _recommendation(40) == "Niedrigere Prioritaet fuer manuelle Pruefung"


def test_calculate_rule_based_score_without_ai() -> None:
    match_result = KeywordMatchResult(
        must_have=[KeywordHit(term="Python", found=True), KeywordHit(term="SQL", found=False)],  # 50%
        nice_to_have=[KeywordHit(term="Docker", found=True)],  # 100%
        keywords=[KeywordHit(term="Git", found=True)],  # 100%
        detected_skills=["Python", "Docker", "Git"],
        missing_must_have=["SQL"],
        missing_nice_to_have=[],
    )

    # Weights: must=40, nice=20, skills=20, seniority=10 (Total non-AI = 90)
    # Must: 0.5 * 40 = 20
    # Nice: 1.0 * 20 = 20
    # Skills: 1.0 * 20 = 20
    # Seniority: text contains "senior", points = 10
    resume_text = "Senior Python Developer"
    
    breakdown = calculate_rule_based_score(
        match_result=match_result,
        resume_text=resume_text,
        ai_fit_score=None,
    )

    # Raw score: 20 + 20 + 20 + 10 = 70 points out of 90.
    # Scaled: (70 / 90) * 100 = 77.77... -> 77.8
    assert breakdown.total_score == 77.8
    assert breakdown.recommendation == "Gute Prioritaet fuer manuelle Pruefung"


def test_calculate_rule_based_score_with_ai() -> None:
    match_result = KeywordMatchResult(
        must_have=[KeywordHit(term="Python", found=True)],  # 100%
        nice_to_have=[],
        keywords=[],
    )

    # Must: 40 points
    # Nice: 20 points (neutral since empty)
    # Skills: 20 points (neutral since empty)
    # Seniority: no text, points = 0
    # AI Score: 8 out of 10
    breakdown = calculate_rule_based_score(
        match_result=match_result,
        resume_text="",
        ai_fit_score=8,
    )

    # Total score: 40 (must) + 20 (nice neutral) + 20 (skills neutral) + 0 (seniority) + 8 (ai) = 88.0
    assert breakdown.total_score == 88.0
    assert breakdown.recommendation == "Hohe Prioritaet fuer manuelle Pruefung"
