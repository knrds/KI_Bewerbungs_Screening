from __future__ import annotations

import json
from unittest.mock import MagicMock
import pytest
from requests import Response
from schemas import KeywordMatchResult, KeywordHit
from ai_analyzer import (
    analyze_resume_with_ai,
    build_fallback_ai_analysis,
)


def test_build_fallback_ai_analysis() -> None:
    match_result = KeywordMatchResult(
        must_have=[KeywordHit(term="Python", found=True), KeywordHit(term="SQL", found=False)],
        nice_to_have=[KeywordHit(term="Docker", found=True)],
        keywords=[KeywordHit(term="Git", found=False)],
        detected_skills=["Python", "Docker"],
        missing_must_have=["SQL"],
        missing_nice_to_have=[],
    )

    fallback = build_fallback_ai_analysis(match_result, reason="API Error")
    
    assert fallback.candidate_summary == "API Error"
    assert fallback.ai_fit_score == 0
    assert fallback.detected_skills.technical == ["Python", "Docker"]
    assert fallback.matched_requirements.must_have == ["Python"]
    assert fallback.matched_requirements.nice_to_have == ["Docker"]
    assert fallback.missing_or_unclear_requirements == ["SQL"]


def test_analyze_resume_no_api_key() -> None:
    match_result = KeywordMatchResult()
    result = analyze_resume_with_ai(
        text="Resume text",
        job_description="Job description",
        match_result=match_result,
        api_key=None,
    )
    assert result.ai_fit_score == 0
    assert "Kein OpenRouter API-Schluessel konfiguriert." in result.candidate_summary


def test_analyze_resume_success(mocker) -> None:
    match_result = KeywordMatchResult(
        must_have=[KeywordHit(term="Python", found=True)],
    )
    
    mock_response_data = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "candidate_name": "Test Candidate",
                        "candidate_summary": "Extremely strong python backend dev.",
                        "detected_skills": {
                            "technical": ["Python", "FastAPI"],
                            "tools": ["Git"],
                            "soft_skills": ["Teamwork"]
                        },
                        "experience_summary": "3 years experience",
                        "matched_requirements": {
                            "must_have": ["Python"],
                            "nice_to_have": [],
                            "keywords": []
                        },
                        "missing_or_unclear_requirements": [],
                        "strengths": ["Strong coding habits"],
                        "weaknesses_or_open_questions": [],
                        "seniority_estimate": "Mid-Level",
                        "ai_fit_score": 9,
                        "ai_score_reasoning": "Fits all criteria.",
                        "interview_questions": {
                            "technical": ["Explain Django middleware"],
                            "experience_based": [],
                            "clarification": []
                        },
                        "evidence": ["Worked at TechCorp for 3 years"],
                        "risk_notes": [],
                        "human_review_recommendation": "Highly recommend interview"
                    })
                }
            }
        ]
    }

    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_data
    mock_post.return_value = mock_response

    result = analyze_resume_with_ai(
        text="Resume of Test Candidate. Python experience.",
        job_description="We need a Python developer.",
        match_result=match_result,
        api_key="valid-key",
        model="openrouter/owl-alpha",
    )

    assert mock_post.called
    assert mock_post.call_args.kwargs["json"]["model"] == "openrouter/owl-alpha"
    assert result.candidate_name == "Test Candidate"
    assert result.ai_fit_score == 9
    assert result.detected_skills.technical == ["Python", "FastAPI"]
    assert result.interview_questions.technical == ["Explain Django middleware"]


def test_analyze_resume_api_error(mocker) -> None:
    match_result = KeywordMatchResult()
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    result = analyze_resume_with_ai(
        text="Resume text",
        job_description="Job description",
        match_result=match_result,
        api_key="valid-key",
    )

    assert result.ai_fit_score == 0
    assert "OpenRouter API Fehler (Status 500)" in result.candidate_summary


def test_analyze_resume_invalid_json(mocker) -> None:
    match_result = KeywordMatchResult()
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "This is not valid JSON content"
                }
            }
        ]
    }
    mock_post.return_value = mock_response

    result = analyze_resume_with_ai(
        text="Resume text",
        job_description="Job description",
        match_result=match_result,
        api_key="valid-key",
    )

    assert result.ai_fit_score == 0
    assert "Fehler beim Parsen der JSON-Antwort" in result.candidate_summary
