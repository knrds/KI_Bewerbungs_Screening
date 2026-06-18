from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ParsedDocument(BaseModel):
    file_name: str
    text: str
    page_count: int
    is_empty: bool = False
    warnings: list[str] = Field(default_factory=list)


class KeywordHit(BaseModel):
    term: str
    found: bool = False
    count: int = 0
    matched_terms: list[str] = Field(default_factory=list)


class KeywordMatchResult(BaseModel):
    must_have: list[KeywordHit] = Field(default_factory=list)
    nice_to_have: list[KeywordHit] = Field(default_factory=list)
    keywords: list[KeywordHit] = Field(default_factory=list)
    detected_skills: list[str] = Field(default_factory=list)
    missing_must_have: list[str] = Field(default_factory=list)
    missing_nice_to_have: list[str] = Field(default_factory=list)
    text_length: int = 0


class ScoreComponent(BaseModel):
    name: str
    points: float
    max_points: float
    explanation: str


class ScoreBreakdown(BaseModel):
    total_score: float = Field(ge=0, le=100)
    components: list[ScoreComponent] = Field(default_factory=list)
    recommendation: str
    explanation: str


class DetectedSkills(BaseModel):
    technical: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)


class MatchedRequirements(BaseModel):
    must_have: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)


class InterviewQuestions(BaseModel):
    technical: list[str] = Field(default_factory=list)
    experience_based: list[str] = Field(default_factory=list)
    clarification: list[str] = Field(default_factory=list)


class AIAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")

    candidate_name: str = ""
    candidate_summary: str = ""
    detected_skills: DetectedSkills = Field(default_factory=DetectedSkills)
    experience_summary: str = ""
    matched_requirements: MatchedRequirements = Field(default_factory=MatchedRequirements)
    missing_or_unclear_requirements: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses_or_open_questions: list[str] = Field(default_factory=list)
    seniority_estimate: str = ""
    ai_fit_score: int = Field(default=0, ge=0, le=10)
    ai_score_reasoning: str = ""
    interview_questions: InterviewQuestions = Field(default_factory=InterviewQuestions)
    evidence: list[str] = Field(default_factory=list)
    risk_notes: list[str] = Field(default_factory=list)
    human_review_recommendation: str = ""


class CandidateEvaluation(BaseModel):
    file_name: str
    candidate_name: str = "Unbekannt"
    parsed_document: ParsedDocument
    keyword_match: KeywordMatchResult
    score: ScoreBreakdown
    ai_analysis: AIAnalysis | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
