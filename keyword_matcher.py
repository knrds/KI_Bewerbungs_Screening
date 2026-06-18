from __future__ import annotations

import re
import unicodedata
from collections.abc import Sequence

from schemas import KeywordHit, KeywordMatchResult


DEFAULT_SYNONYMS: dict[str, list[str]] = {
    "javascript": ["js", "java script"],
    "typescript": ["ts", "type script"],
    "react": ["react.js", "reactjs"],
    "node.js": ["node", "nodejs"],
    "postgresql": ["postgres", "postgres sql", "sql database"],
    "machine learning": ["ml", "ki", "ai"],
    "rest api": ["rest", "restful api"],
    "docker": ["container", "containers"],
    "aws": ["amazon web services"],
    "project management": ["projektmanagement", "project manager"],
    "communication": ["kommunikation"],
}


def split_terms(value: str | Sequence[str] | None) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        raw_terms = re.split(r"[,;\n]", value)
    else:
        raw_terms = list(value)

    return _unique_clean_terms(raw_terms)


def match_candidate_text(
    text: str,
    must_have: str | Sequence[str] | None = None,
    nice_to_have: str | Sequence[str] | None = None,
    keywords: str | Sequence[str] | None = None,
    synonyms: dict[str, list[str]] | None = None,
) -> KeywordMatchResult:
    normalized_text = normalize_for_matching(text)
    synonym_map = _normalize_synonym_map(synonyms or DEFAULT_SYNONYMS)

    must_terms = split_terms(must_have)
    nice_terms = split_terms(nice_to_have)
    keyword_terms = split_terms(keywords)

    must_hits = [_match_term(normalized_text, term, synonym_map) for term in must_terms]
    nice_hits = [_match_term(normalized_text, term, synonym_map) for term in nice_terms]
    keyword_hits = [_match_term(normalized_text, term, synonym_map) for term in keyword_terms]

    detected_skills = _unique_clean_terms(
        hit.term
        for hit in [*must_hits, *nice_hits, *keyword_hits]
        if hit.found
    )

    return KeywordMatchResult(
        must_have=must_hits,
        nice_to_have=nice_hits,
        keywords=keyword_hits,
        detected_skills=detected_skills,
        missing_must_have=[hit.term for hit in must_hits if not hit.found],
        missing_nice_to_have=[hit.term for hit in nice_hits if not hit.found],
        text_length=len(text),
    )


def normalize_for_matching(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9+#.]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _match_term(
    normalized_text: str,
    term: str,
    synonyms: dict[str, list[str]],
) -> KeywordHit:
    normalized_term = normalize_for_matching(term)
    variants = [normalized_term, *synonyms.get(normalized_term, [])]
    variants = _unique_clean_terms(variants)

    matched_terms = []
    total_count = 0
    for variant in variants:
        count = _count_phrase(normalized_text, variant)
        if count:
            matched_terms.append(variant)
            total_count += count

    return KeywordHit(
        term=term,
        found=total_count > 0,
        count=total_count,
        matched_terms=matched_terms,
    )


def _count_phrase(normalized_text: str, normalized_phrase: str) -> int:
    if not normalized_phrase:
        return 0

    pattern = rf"(?<![a-z0-9]){re.escape(normalized_phrase)}(?![a-z0-9])"
    return sum(
        1
        for match in re.finditer(pattern, normalized_text)
        if not _is_negated_match(normalized_text, match.start(), match.end())
    )


def _is_negated_match(normalized_text: str, start: int, end: int) -> bool:
    preceding_tokens = normalized_text[:start].split()[-10:]
    following_tokens = normalized_text[end:].split()[:4]
    before = " ".join(preceding_tokens)
    after = " ".join(following_tokens)

    negation_terms = {
        "kein",
        "keine",
        "keinen",
        "keiner",
        "ohne",
        "nicht",
        "no",
        "without",
        "missing",
    }
    if any(token in negation_terms for token in preceding_tokens[-4:]):
        return True

    negative_followups = [
        "fehlt",
        "fehlen",
        "nicht vorhanden",
        "nicht belegt",
        "not present",
        "not proven",
    ]
    if any(phrase in after for phrase in negative_followups):
        return True

    negative_contexts = [
        "keine praxis",
        "keine belegte praxis",
        "keine erfahrung",
        "keine belegte erfahrung",
        "ohne erfahrung",
        "ohne belegte erfahrung",
        "no experience",
        "without experience",
    ]
    return any(context in before for context in negative_contexts)


def _normalize_synonym_map(synonyms: dict[str, list[str]]) -> dict[str, list[str]]:
    return {
        normalize_for_matching(key): [
            normalize_for_matching(value)
            for value in values
            if normalize_for_matching(value)
        ]
        for key, values in synonyms.items()
        if normalize_for_matching(key)
    }


def _unique_clean_terms(terms: Sequence[str]) -> list[str]:
    cleaned_terms = []
    seen = set()
    for term in terms:
        cleaned = str(term).strip()
        if not cleaned:
            continue

        identity = normalize_for_matching(cleaned)
        if identity in seen:
            continue

        seen.add(identity)
        cleaned_terms.append(cleaned)

    return cleaned_terms
