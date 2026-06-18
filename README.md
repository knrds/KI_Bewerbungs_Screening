# AI Resume Screening & Candidate Ranking Workflow

Kleine Streamlit-App fuer die strukturierte Voranalyse von Bewerbungen.

Das System soll Recruiter und Projektleiter bei der manuellen Pruefung
unterstuetzen. Es trifft keine automatische Annahme- oder
Ablehnungsentscheidung.

## MVP-Ziel

- PDF-Lebenslaeufe einlesen
- Keywords, Muss-Kriterien und Wunsch-Kriterien erkennen
- erklaerbaren Fit Score berechnen
- optional OpenRouter fuer eine strukturierte KI-Analyse nutzen
- mehrere Bewerbungen als Ranking anzeigen
- Ergebnisse als JSON oder Markdown exportieren

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

## Demo-Szenario

Im Dashboard kann direkt `Demo-Szenario laden & analysieren` genutzt werden.
Die App lädt dann die Beispiel-Stellenbeschreibung, Beispiel-Kriterien und drei
Fake-Lebensläufe aus `sample_data/fake_resumes/`. Ohne OpenRouter API-Key läuft
die Demo im regelbasierten Fallback-Modus.

## Projektstruktur

```text
app.py              Streamlit UI
config.py           Konfiguration, Modelle, Score-Gewichte
pdf_parser.py       PDF-Text-Extraktion
keyword_matcher.py  Keyword-, Skill- und Synonym-Matching
scoring.py          Regelbasierter Fit Score
ai_analyzer.py      OpenRouter-Integration
ranking.py          Ranking-Tabelle
schemas.py          Pydantic-Datenmodelle
export_utils.py     JSON- und Markdown-Export
sample_data/        Demo-Daten
```

## Sicherheitsprinzipien

- Keine automatische Ablehnung
- Keine finale Einstellungsentscheidung
- Keine Bewertung sensibler Merkmale
- Keine dauerhafte Speicherung echter Bewerberdaten im MVP
- Jeder Score muss nachvollziehbar sein
