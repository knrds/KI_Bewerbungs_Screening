# INITIALISIERUNG.md

# Projekt: AI Resume Screening & Candidate Ranking Workflow

## Rolle des KI-Agenten

Du bist ein erfahrener Full-Stack-Entwickler, KI-Automation-Consultant, technischer Projektmanager und Entwicklungscoach.

Du sollst ein kleines, aber professionell vorzeigbares KI-/Automatisierungsprojekt entwickeln, das als Portfolio-Projekt, Bewerbungsprojekt oder Demo für praktische Unternehmensanwendungen genutzt werden kann.

Das Projekt soll pragmatisch, verständlich, technisch sauber und realistisch umsetzbar sein.

---

# 1. Projektidee

Das Projekt heißt:

**AI Resume Screening & Candidate Ranking Workflow**

Die Anwendung soll Bewerbungen automatisiert voranalysieren.

Ein Nutzer soll eine oder mehrere Bewerbungen hochladen können. Eine Bewerbung kann bestehen aus:

- PDF-Lebenslauf
- optionalem Anschreiben
- optionalen Zusatzinformationen
- optionaler Stellenbeschreibung
- optionalen geforderten Keywords, Skills oder Muss-Kriterien

Das System extrahiert die Inhalte, analysiert diese und erstellt daraus eine strukturierte Bewertung.

Das Ziel ist nicht, Bewerber automatisch abzulehnen oder finale Personalentscheidungen zu treffen.
Das Ziel ist ein Assistenzsystem, das Recruiter, HR-Mitarbeiter oder Projektleiter bei der strukturierten Voranalyse unterstützt.

Die finale Entscheidung muss immer bei einem Menschen liegen.

---

# 2. Hauptziel des Projekts

Das Tool soll Bewerbungen strukturiert analysieren und priorisieren.

Es soll erkennen:

- Welche Skills der Bewerber mitbringt
- Welche geforderten Keywords oder Technologien vorhanden sind
- Welche Anforderungen aus der Stellenbeschreibung erfüllt werden
- Welche Anforderungen fehlen oder unklar sind
- Wie gut der Bewerber zur Stelle passt
- Welche Stärken sichtbar sind
- Welche offenen Punkte im Interview geklärt werden sollten
- Welche Bewerbung im Vergleich zu anderen Bewerbungen am besten zur Stelle passt

Das Ergebnis soll ein Ranking-System sein.

Wichtig:
Der Score ist kein echter Annahme-Wahrscheinlichkeitswert und keine finale Entscheidung.
Der Score ist ein **Fit Score**, der ausdrückt, wie gut die Bewerbung anhand der verfügbaren Informationen zu den definierten Anforderungen passt.

---

# 3. Konkreter Use Case

Ein Unternehmen erhält mehrere Bewerbungen auf eine Stelle.

Normalerweise müsste ein Recruiter jeden Lebenslauf manuell lesen, Skills suchen, Anforderungen vergleichen, Notizen machen und Kandidaten priorisieren.

Dieses Tool automatisiert diesen Voranalyse-Prozess.

Ablauf:

1. Nutzer gibt eine Stellenbeschreibung ein.
2. Nutzer gibt Muss-Kriterien, Wunsch-Kriterien und Keywords ein.
3. Nutzer lädt einen oder mehrere PDF-Lebensläufe hoch.
4. Das System extrahiert den Text.
5. Das System sucht nach geforderten Keywords und Skills.
6. Das System bewertet jede Bewerbung nach einem nachvollziehbaren Scoring-System.
7. Optional prüft ein KI-Modell über OpenRouter die Bewerbung zusätzlich semantisch.
8. Das System erstellt eine Rangliste.
9. Die passendsten Bewerbungen stehen oben.
10. Zu jeder Bewerbung gibt es eine Kurzbegründung, Score-Erklärung und Interviewfragen.

---

# 4. Wichtige Grundregel

Das Projekt darf nicht als automatisches Aussortierungs- oder Ablehnungssystem gebaut werden.

Stattdessen soll es so formuliert und umgesetzt werden:

- Bewerber werden nicht automatisch abgelehnt.
- Bewerber werden nicht endgültig angenommen.
- Das System erstellt nur eine strukturierte Priorisierung.
- Der Score ist eine Entscheidungshilfe.
- Der Mensch trifft die finale Entscheidung.
- Sensible Merkmale dürfen nicht bewertet werden.
- Alter, Geschlecht, Herkunft, Religion, Foto, Familienstand oder ähnliche Merkmale dürfen nicht in die Bewertung einfließen.
- Wenn Informationen fehlen, muss das System diese als offene Punkte markieren.

---

# 5. MVP-Ziel

Die erste Version soll bewusst klein bleiben.

Das MVP soll Folgendes können:

- Streamlit-Webapp starten
- eine Stellenbeschreibung eingeben
- geforderte Keywords eingeben
- PDF-Lebensläufe hochladen
- Text aus PDFs extrahieren
- Keywords und Skills im Text erkennen
- einfache regelbasierte Bewertung erzeugen
- optional KI-Bewertung über OpenRouter starten
- strukturierten Score berechnen
- Bewerbungen nach Score sortieren
- Ergebnis als Ranking-Tabelle anzeigen
- pro Bewerber eine kurze Zusammenfassung anzeigen
- Begründung für den Score anzeigen
- Interviewfragen generieren
- Ergebnis als JSON oder Markdown exportieren

---

# 6. Tech Stack

Nutze für Version 1 folgenden Tech Stack:

- Python
- Streamlit für die Benutzeroberfläche
- PyMuPDF für PDF Parsing
- OpenRouter API für KI-Auswertung
- Pydantic oder JSON Schema für strukturierte KI-Ausgaben
- Pandas für Ranking-Tabellen
- dotenv für API-Key-Verwaltung
- JSON oder Markdown für Export

Keine komplexe Datenbank in Version 1.
Kein Login-System in Version 1.
Keine dauerhafte Speicherung echter Bewerberdaten in Version 1.

---

# 7. OpenRouter-Integration

Das System soll eine OpenRouter-Integration enthalten.

Der Nutzer soll in der App einen OpenRouter API Key angeben können oder alternativ den Key über eine `.env`-Datei laden.

Der Nutzer soll außerdem ein Modell auswählen oder manuell eintragen können.

Standardmodell für die Demo:

```text
moonshotai/kimi-k2.6:free
```

Zusätzlich soll das System so gebaut sein, dass andere OpenRouter-Modelle leicht austauschbar sind.

Beispiele für mögliche Modell-IDs:

```text
moonshotai/kimi-k2.6:free
openrouter/free
anthropic/claude-sonnet-4
openai/gpt-4.1
google/gemini-2.5-pro
```

Die konkrete Modellliste kann sich ändern. Deshalb soll das Modell nicht hart im Code versteckt werden, sondern über Konfiguration oder UI auswählbar sein.

---

# 8. Fallback-Logik

Das Tool braucht eine einfache Fallback-Logik.

Falls kein API-Key vorhanden ist, das Modell nicht erreichbar ist oder die KI-Auswertung fehlschlägt, soll das System trotzdem eine Basisanalyse durchführen.

Fallback-Version:

- PDF-Text extrahieren
- Keywords zählen
- Muss-Kriterien prüfen
- Wunsch-Kriterien prüfen
- einfache Skill-Liste anhand Keyword-Matching erstellen
- regelbasierten Score berechnen
- Ergebnis in Ranking-Tabelle anzeigen

Dadurch bleibt das Tool auch ohne KI teilweise funktionsfähig.

Die KI ist also eine Erweiterung, aber nicht die einzige Grundlage des Systems.

---

# 9. Scoring-System

Das Projekt soll ein nachvollziehbares Scoring-System verwenden.

Der Score soll von 0 bis 100 gehen.

Beispielgewichtung für Version 1:

```text
Muss-Kriterien erfüllt: 40 Punkte
Wunsch-Kriterien erfüllt: 20 Punkte
Technologie-/Skill-Match: 20 Punkte
Berufserfahrung / Seniorität: 10 Punkte
KI-semantische Bewertung: 10 Punkte
```

Wenn keine KI verfügbar ist, werden die 10 KI-Punkte entweder weggelassen oder durch eine neutrale Regelbewertung ersetzt.

Der Score darf nicht willkürlich sein.
Jeder Score muss erklärbar sein.

Zu jedem Bewerber soll angezeigt werden:

- Gesamtscore
- erfüllte Muss-Kriterien
- fehlende Muss-Kriterien
- gefundene Keywords
- relevante Skills
- kurze Zusammenfassung
- Score-Begründung
- offene Fragen
- empfohlene Interviewfragen

---

# 10. Keyword- und Skill-Matching

Das System soll nach Keywords suchen, die in der Stellenbeschreibung oder manuell durch den Nutzer angegeben wurden.

Keyword-Arten:

- Muss-Kriterien
- Wunsch-Kriterien
- Technologien
- Tools
- Soft Skills
- Zertifikate
- Branchenbegriffe

Beispiele:

```text
Python
JavaScript
React
SQL
Docker
AWS
Machine Learning
REST API
Git
Scrum
Kommunikation
Projektmanagement
```

Das Matching soll nicht nur exakte Treffer zählen, sondern möglichst auch einfache Varianten erkennen.

Beispiele:

```text
JavaScript = JS
TypeScript = TS
React.js = React
PostgreSQL = SQL-Datenbank
Machine Learning = ML
```

Für Version 1 reicht eine einfache Synonymliste im Code.

---

# 11. KI-Komponente

Die KI soll nicht blind entscheiden, sondern eine strukturierte Analyse liefern.

Die KI bekommt:

- extrahierten Lebenslauftext
- optionales Anschreiben
- Stellenbeschreibung
- Muss-Kriterien
- Wunsch-Kriterien
- gefundene Keywords
- Ergebnis der regelbasierten Voranalyse

Die KI soll daraus erzeugen:

- Kurzprofil
- wichtigste Skills
- relevante Erfahrung
- Einschätzung zur Passung
- offene Punkte
- mögliche Schwächen
- Score-Erklärung
- Interviewfragen
- Hinweise, welche Aussagen aus dem Lebenslauf belegt sind
- Hinweis, welche Informationen fehlen

Die KI darf keine nicht belegten Skills erfinden.

Wenn eine Information nicht im Lebenslauf steht, soll sie schreiben:

```text
Nicht im Lebenslauf gefunden.
```

---

# 12. Strukturierte KI-Ausgabe

Die KI-Ausgabe soll als JSON erzeugt werden.

Gewünschtes Schema:

```json
{
  "candidate_name": "",
  "candidate_summary": "",
  "detected_skills": {
    "technical": [],
    "tools": [],
    "soft_skills": []
  },
  "experience_summary": "",
  "matched_requirements": {
    "must_have": [],
    "nice_to_have": [],
    "keywords": []
  },
  "missing_or_unclear_requirements": [],
  "strengths": [],
  "weaknesses_or_open_questions": [],
  "seniority_estimate": "",
  "ai_fit_score": 0,
  "ai_score_reasoning": "",
  "interview_questions": {
    "technical": [],
    "experience_based": [],
    "clarification": []
  },
  "evidence": [],
  "risk_notes": [],
  "human_review_recommendation": ""
}
```

Die Anwendung soll versuchen, die KI-Ausgabe zu validieren.
Falls das JSON ungültig ist, soll eine Fallback-Ausgabe angezeigt werden.

---

# 13. Ranking-Ausgabe

Wenn mehrere Bewerbungen hochgeladen werden, soll das Tool eine Ranking-Tabelle anzeigen.

Spalten:

- Rang
- Bewerber
- Gesamtscore
- Muss-Kriterien erfüllt
- Wunsch-Kriterien erfüllt
- Keyword-Matches
- KI-Score
- Kurzprofil
- offene Punkte
- Empfehlung für manuelle Prüfung

Beispiel:

```text
Rang 1 | Max Mustermann | 87/100 | starke Übereinstimmung | Interview empfohlen
Rang 2 | Erika Beispiel | 74/100 | gute Übereinstimmung | manuell prüfen
Rang 3 | Alex Demo | 52/100 | mehrere Lücken | nur bei Bedarf prüfen
```

Wichtig:

Die Ausgabe darf nicht lauten:

```text
Bewerber ablehnen
```

Besser:

```text
Niedrigere Priorität für manuelle Prüfung
```

---

# 14. Empfohlene Projektstruktur

Erstelle das Projekt mit folgender Struktur:

```text
ai-resume-ranking/
│
├── app.py
├── config.py
├── pdf_parser.py
├── keyword_matcher.py
├── scoring.py
├── ai_analyzer.py
├── ranking.py
├── schemas.py
├── export_utils.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── sample_data/
    ├── sample_job_description.txt
    ├── sample_keywords.json
    └── fake_resumes/
```

Aufgaben der Dateien:

```text
app.py
- Streamlit UI
- Datei-Upload
- Eingabefelder
- Ergebnisanzeige

config.py
- Modellname
- API-Key-Handling
- Standardkonfiguration

pdf_parser.py
- PDF-Text extrahieren
- leere PDFs erkennen

keyword_matcher.py
- Keywords suchen
- Muss-Kriterien prüfen
- Wunsch-Kriterien prüfen
- Synonyme berücksichtigen

scoring.py
- regelbasierten Score berechnen
- Gewichtung verwalten

ai_analyzer.py
- OpenRouter API ansprechen
- Prompt erstellen
- KI-Antwort verarbeiten

ranking.py
- Ergebnisse mehrerer Bewerbungen sortieren
- Ranking-Tabelle erzeugen

schemas.py
- Pydantic-Modelle oder JSON-Schemas

export_utils.py
- Export als JSON oder Markdown

README.md
- Projektdokumentation
```

---

# 15. Workflow

Der Workflow soll so funktionieren:

```text
Input
→ Stellenbeschreibung
→ Muss-Kriterien
→ Wunsch-Kriterien
→ Keyword-Liste
→ ein oder mehrere PDF-Lebensläufe

Verarbeitung
→ PDF-Text extrahieren
→ Text bereinigen
→ Keywords erkennen
→ Muss-/Wunsch-Kriterien prüfen
→ regelbasierten Score berechnen

KI-Auswertung
→ OpenRouter-Modell analysiert Bewerbung
→ KI erstellt strukturierte Einschätzung
→ KI liefert Score-Erklärung und Interviewfragen

Ranking
→ Regelbasierter Score + KI-Score werden kombiniert
→ Bewerbungen werden sortiert
→ passendste Bewerbungen stehen oben

Ausgabe
→ Ranking-Tabelle
→ Detailansicht pro Bewerbung
→ Score-Erklärung
→ Interviewfragen
→ Export als JSON/Markdown

Möglicher Folgeprozess
→ HR prüft Top-Kandidaten manuell
→ Interview wird vorbereitet
→ Ergebnis kann dokumentiert werden
```

---

# 16. Roadmap

## Phase 1: Schnell umsetzbare Demo

Ziel: Eine funktionierende lokale Streamlit-App.

Features:

- PDF-Upload für einen Lebenslauf
- Stellenbeschreibung als Textfeld
- manuelle Keyword-Eingabe
- PDF-Text-Extraktion
- Keyword-Matching
- einfacher Score von 0 bis 100
- OpenRouter API-Key über `.env`
- KI-Analyse mit einem konfigurierbaren Modell
- strukturierte Ergebnisanzeige
- keine Speicherung echter Bewerberdaten

Erfolgskriterium:

Die App kann einen Lebenslauf analysieren und einen nachvollziehbaren Fit Score mit Begründung ausgeben.

---

## Phase 2: Verbesserte Portfolio-Version

Ziel: Das Projekt wirkt wie ein echtes kleines Produkt.

Features:

- mehrere PDFs gleichzeitig hochladen
- Ranking-Tabelle aller Bewerbungen
- Muss-/Wunsch-Kriterien getrennt gewichten
- Synonyme für Skill-Matching
- Modell-Auswahl in der UI
- OpenRouter API-Key optional in der UI eingebbar
- Export als JSON und Markdown
- schöneres Streamlit-Layout
- Fake-Beispieldaten
- README mit Screenshots
- Architekturdiagramm
- Fehlerbehandlung bei kaputten oder leeren PDFs
- Hinweis auf Human-in-the-loop und Datenschutz

Erfolgskriterium:

Das Projekt ist auf GitHub und in einem Bewerbungsgespräch gut erklärbar.

---

## Phase 3: Professionellere Unternehmens-Version

Ziel: Erweiterung zu einem glaubwürdigen HR-Workflow.

Features:

- OCR für eingescannte PDFs
- PDF-Report-Export
- CSV-Export für HR-Tools
- Google Sheets oder Airtable-Anbindung
- n8n-Workflow für automatische Weiterverarbeitung
- Kandidatenhistorie mit lokaler Datenbank
- Audit-Log für Bewertungen
- Bias-/Compliance-Check
- Rollenmodell
- manuelle Freigabe durch HR
- klare Datenschutz- und Löschlogik

Erfolgskriterium:

Das Projekt kann als realistischer Unternehmensprototyp präsentiert werden.

---

# 17. Sicherheits- und Qualitätsregeln

Das System muss folgende Regeln einhalten:

- Keine automatische Ablehnung.
- Keine finale Einstellungsentscheidung.
- Keine Bewertung sensibler Merkmale.
- Keine Analyse von Fotos.
- Keine Bewertung von Alter, Herkunft, Geschlecht, Religion oder Familienstand.
- Keine Speicherung echter Bewerberdaten im MVP.
- Jeder Score muss erklärbar sein.
- KI-Aussagen müssen möglichst mit Belegen aus dem Lebenslauf verbunden werden.
- Fehlende Informationen müssen als offen oder unklar markiert werden.
- Die UI muss klar anzeigen, dass es sich um eine Entscheidungshilfe handelt.

---

# 18. Akzeptanzkriterien für Version 1

Version 1 gilt als fertig, wenn:

- die App mit `streamlit run app.py` startet
- ein PDF hochgeladen werden kann
- Text aus dem PDF extrahiert wird
- Keywords erkannt werden
- ein regelbasierter Score berechnet wird
- OpenRouter optional genutzt werden kann
- das Modell konfigurierbar ist
- eine strukturierte KI-Auswertung angezeigt wird
- der Bewerber nicht automatisch abgelehnt wird
- der Score nachvollziehbar erklärt wird
- die Ergebnisse als JSON oder Markdown exportiert werden können
- das Projekt eine verständliche README besitzt

---

# 19. Entwicklungsreihenfolge

Arbeite in dieser Reihenfolge:

1. Projektstruktur erstellen
2. requirements.txt erstellen
3. `.env.example` erstellen
4. PDF-Parser bauen
5. Keyword-Matcher bauen
6. Scoring-System bauen
7. Streamlit UI für Einzelanalyse bauen
8. OpenRouter API-Anbindung bauen
9. KI-Prompt und JSON-Schema bauen
10. Ergebnisanzeige verbessern
11. Multi-PDF-Upload einbauen
12. Ranking-Tabelle bauen
13. Export-Funktion bauen
14. Fehlerbehandlung verbessern
15. README schreiben
16. Beispiel-Daten hinzufügen

Wichtig:

Beginne nicht direkt mit allen Features.
Baue zuerst eine stabile Einzelanalyse.
Erweitere danach auf mehrere Bewerbungen und Ranking.

---

# 20. Erste Aufgabe für den KI-Agenten

Erstelle zuerst nur:

1. eine technische Gesamtarchitektur
2. die finale Projektstruktur
3. den Datenfluss
4. die genaue Implementierungsreihenfolge
5. eine kurze Erklärung, welche Dateien zuerst gebaut werden sollen

Schreibe noch keinen vollständigen Code.

Warte danach auf die nächste Anweisung.

Ziel ist ein kleines, sauberes, vorzeigbares Projekt, kein überkomplexes HR-System.
