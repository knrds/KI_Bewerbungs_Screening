# AI Resume Screening & Candidate Ranking Workflow

Streamlit-Demo fuer eine nachvollziehbare Voranalyse von PDF-Bewerbungen. Die App vergleicht Lebenslaeufe mit Stellenanforderungen, berechnet einen erklaerbaren Fit Score und zeigt ein priorisiertes Ranking mit Kandidatendetails, offenen Punkten, Belegen und Interviewfragen.

Die Anwendung ist als Portfolio- und MVP-Projekt gedacht: Sie unterstuetzt die manuelle Pruefung, trifft aber keine Annahme- oder Ablehnungsentscheidung.

## Funktionen

- PDF-Lebenslaeufe einlesen und Text extrahieren
- Muss-Kriterien, Wunsch-Kriterien und Keywords matchen
- Fit Score mit erklaerbaren Score-Komponenten berechnen
- Kandidatenranking mit Status, Skill Match und Detailansicht anzeigen
- Fallback-Modus ohne API-Key ueber regelbasiertes Scoring nutzen
- Optional OpenRouter fuer strukturierte KI-Analysen einbinden
- Score-Gewichtung und Modell-ID in der UI einstellen
- Ergebnisse als JSON oder Markdown exportieren

## Demo-Szenario

Im Dashboard kann `Demo-Szenario analysieren` direkt gestartet werden. Die App laedt dann eine Beispielrolle, passende Kriterien und sieben synthetische PDF-Lebenslaeufe aus `sample_data/fake_resumes/`.

Die Samples decken typische und extreme Faelle ab:

- sehr starker Full-Stack-Fit
- solider Backend-Fit mit Luecken
- Junior-Profil mit niedrigem Match
- Synonym-Fall fuer RESTful API, PostgreSQL, React.js und Amazon Web Services
- Management-Profil mit vielen Soft Skills, aber wenig Hands-on-Technik
- Data-Analyst-Profil mit Teilmatch
- leeres/scanned-style PDF ohne extrahierbaren Text

Ohne OpenRouter API-Key laeuft die Demo vollstaendig im regelbasierten Fallback-Modus und zeigt `Fallback aktiv`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Optional kann in `.env` oder in den App-Einstellungen ein OpenRouter API-Key gesetzt werden:

```bash
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=moonshotai/kimi-k2.6:free
```

## Tests

```bash
python -m py_compile app.py sample_data/fake_resumes/generate_fake_resumes.py
pytest -q
```

Die Demo-PDFs koennen bei Bedarf neu erzeugt werden:

```bash
python sample_data/fake_resumes/generate_fake_resumes.py
```

## Projektstruktur

```text
app.py                                Streamlit UI und App-State
config.py                             Konfiguration, Modelle, Score-Gewichte
pdf_parser.py                         PDF-Text-Extraktion
keyword_matcher.py                    Keyword-, Skill- und Synonym-Matching
scoring.py                            Regelbasierter Fit Score
ai_analyzer.py                        OpenRouter-Integration
ranking.py                            Ranking-Hilfen
schemas.py                            Pydantic-Datenmodelle
export_utils.py                       JSON- und Markdown-Export
sample_data/                          Demo-Stellenbeschreibung und Kriterien
sample_data/fake_resumes/             Synthetische Demo-Lebenslaeufe
tests/                                Unit-Tests fuer Kernlogik und Samples
```

## Sicherheitsprinzipien

- Keine automatische Annahme oder Ablehnung
- Finale Entscheidung immer durch einen Menschen
- Keine Bewertung sensibler Merkmale wie Alter, Herkunft, Geschlecht, Religion oder Foto
- Keine dauerhafte Speicherung echter Bewerberdaten im MVP
- Jeder Score muss nachvollziehbar und als Entscheidungshilfe gekennzeichnet sein
