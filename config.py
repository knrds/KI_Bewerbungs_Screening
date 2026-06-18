from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "moonshotai/kimi-k2.6:free")

MODEL_OPTIONS = [
    "moonshotai/kimi-k2.6:free",
    "openrouter/free",
    "anthropic/claude-sonnet-4",
    "openai/gpt-4.1",
    "google/gemini-2.5-pro",
]

SENSITIVE_ATTRIBUTES = [
    "age",
    "gender",
    "origin",
    "religion",
    "family_status",
    "photo",
    "health",
]

HUMAN_REVIEW_NOTICE = (
    "Dieses Tool erstellt nur eine strukturierte Voranalyse. "
    "Es trifft keine Einstellungs- oder Ablehnungsentscheidung."
)


@dataclass(frozen=True)
class ScoreWeights:
    must_have: int = 40
    nice_to_have: int = 20
    skills: int = 20
    seniority: int = 10
    ai_semantic: int = 10

    @property
    def total(self) -> int:
        return (
            self.must_have
            + self.nice_to_have
            + self.skills
            + self.seniority
            + self.ai_semantic
        )

    @property
    def total_without_ai(self) -> int:
        return self.total - self.ai_semantic


DEFAULT_SCORE_WEIGHTS = ScoreWeights()


def get_openrouter_api_key(user_provided_key: str | None = None) -> str | None:
    key = user_provided_key or os.getenv("OPENROUTER_API_KEY")
    if not key:
        return None
    return key.strip() or None
