from __future__ import annotations

import json
import requests
from config import OPENROUTER_BASE_URL, DEFAULT_MODEL
from schemas import AIAnalysis, DetectedSkills, KeywordMatchResult, MatchedRequirements, KeywordHit


def build_fallback_ai_analysis(
    match_result: KeywordMatchResult,
    reason: str = "KI-Auswertung nicht verfuegbar.",
) -> AIAnalysis:
    return AIAnalysis(
        candidate_summary=reason,
        detected_skills=DetectedSkills(
            technical=match_result.detected_skills,
            tools=[],
            soft_skills=[],
        ),
        matched_requirements=MatchedRequirements(
            must_have=[
                hit.term for hit in match_result.must_have if hit.found
            ],
            nice_to_have=[
                hit.term for hit in match_result.nice_to_have if hit.found
            ],
            keywords=[
                hit.term for hit in match_result.keywords if hit.found
            ],
        ),
        missing_or_unclear_requirements=[
            *match_result.missing_must_have,
            *match_result.missing_nice_to_have,
        ],
        ai_fit_score=0,
        ai_score_reasoning=reason,
        human_review_recommendation="Manuelle Pruefung erforderlich.",
    )


def analyze_resume_with_ai(
    text: str,
    job_description: str,
    match_result: KeywordMatchResult,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> AIAnalysis:
    if not api_key:
        return build_fallback_ai_analysis(
            match_result,
            reason="Kein OpenRouter API-Schluessel konfiguriert."
        )

    system_prompt = (
        "Du bist ein erfahrener HR-Assistent und Experte fuer die strukturierte Voranalyse von Bewerbungsunterlagen. "
        "Deine Aufgabe ist es, den bereitgestellten Lebenslauftext mit einer Stellenbeschreibung und spezifischen Anforderungen abzugleichen.\n\n"
        "WICHTIGE COMPLIANCE-REGELN:\n"
        "- Bewerte NIEMALS sensible persoenliche Merkmale wie Alter, Geschlecht, Herkunft, Religion, Foto, Familienstand, ethnische Zugehoerigkeit oder Behinderung. Falls solche Daten im Lebenslauf vorhanden sind, MUESSEN sie vollstaendig ignoriert werden.\n"
        "- Triff keine finalen Annahme- oder Ablehnungsentscheidungen. Deine Auswertung dient rein als strukturierte Entscheidungshilfe.\n"
        "- Jede Feststellung muss auf Fakten aus dem bereitgestellten Text beruhen. Erfinde keine Kompetenzen oder Erfahrungen.\n"
        "- Wenn Informationen unklar sind oder fehlen, trage diese unter 'missing_or_unclear_requirements' oder 'weaknesses_or_open_questions' ein.\n\n"
        "Antworte AUSSCHLIESSLICH im JSON-Format, das der Struktur dieses Pydantic/JSON-Schemas entspricht:\n"
        f"{json.dumps(AIAnalysis.model_json_schema(), ensure_ascii=False)}"
    )

    user_prompt = (
        f"Stellenbeschreibung:\n{job_description}\n\n"
        f"Geforderte Muss-Kriterien:\n{', '.join([h.term for h in match_result.must_have])}\n"
        f"Geforderte Wunsch-Kriterien:\n{', '.join([h.term for h in match_result.nice_to_have])}\n"
        f"Geforderte Keywords:\n{', '.join([h.term for h in match_result.keywords])}\n\n"
        f"Bereits gefundene Kriterien (aus regelbasierter Analyse):\n"
        f"- Gefundene Muss-Kriterien: {', '.join([h.term for h in match_result.must_have if h.found]) or 'keine'}\n"
        f"- Gefundene Wunsch-Kriterien: {', '.join([h.term for h in match_result.nice_to_have if h.found]) or 'keine'}\n"
        f"- Gefundene Keywords: {', '.join([h.term for h in match_result.keywords if h.found]) or 'keine'}\n\n"
        f"Lebenslauf-Text:\n{text}\n\n"
        "Bitte analysiere den Lebenslauf-Text im Kontext der Anforderungen und fuelle das JSON-Schema vollstaendig aus."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Antigravity/ai-resume-screening",
        "X-Title": "AI Resume Screening",
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
    }

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        if response.status_code != 200:
            return build_fallback_ai_analysis(
                match_result,
                reason=f"OpenRouter API Fehler (Status {response.status_code}): {response.text}"
            )
        
        response_json = response.json()
        choices = response_json.get("choices", [])
        if not choices:
            return build_fallback_ai_analysis(
                match_result,
                reason="Keine Antwort vom Modell erhalten."
            )
        
        content = choices[0].get("message", {}).get("content", "")
        if not content:
            return build_fallback_ai_analysis(
                match_result,
                reason="Modell lieferte leeren Text zurueck."
            )
        
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed_data = json.loads(content)
        
        return AIAnalysis.model_validate(parsed_data)
        
    except json.JSONDecodeError as exc:
        return build_fallback_ai_analysis(
            match_result,
            reason=f"Fehler beim Parsen der JSON-Antwort des LLMs: {exc}"
        )
    except Exception as exc:
        return build_fallback_ai_analysis(
            match_result,
            reason=f"Fehler bei der KI-Analyse: {exc}"
        )
