# 🧠 AI Resume Screening & Candidate Ranking Workflow

Dieses Projekt ist ein professioneller, voll funktionsfähiger Portfolio-Prototyp zur intelligenten Voranalyse von Bewerbungsunterlagen. Die Anwendung liest PDF-Lebensläufe ein, gleicht sie mit Stellenanforderungen ab, berechnet einen nachvollziehbaren **Fit Score** und visualisiert ein priorisiertes Ranking in einem modernen Web-Interface.

Das System kombiniert ein präzises, regelbasiertes Keyword-Matching (inkl. Synonymerkennung) mit einer semantischen LLM-Analyse via **OpenRouter** (z. B. mit kostenlosen Modellen wie `openrouter/owl-alpha` oder `moonshotai/kimi-k2.6:free`).

---

## 🌟 Stärken des Projekts

- **Hybrider Analyseansatz:** Verknüpft klassisches, robustes Keyword- und Skill-Matching (mit automatischer Erkennung von Synonymen wie „container“ für „Docker“ oder „AWS“ für „Cloud“) mit fortschrittlicher semantischer LLM-Voranalyse.
- **Vollständige State-Persistenz:** Durch ein maßgeschneidertes State-Management in Streamlit gehen Benutzereingaben, API-Konfigurationen, das ausgewählte KI-Modell sowie aktive Filter- und Sucheinstellungen beim Wechseln zwischen den Tabs niemals verloren.
- **Feingliedrige Risikoerkennung (Tie-Breaker):** Die KI analysiert Details wie Überqualifizierungsrisiken (z. B. bei Senior-Profilen für Junior-Rollen) oder Technologielücken und nutzt diese für eine differenzierte Bewertung, um Gleichstände aus dem reinen Keyword-Matching aufzulösen.
- **Human-in-the-Loop & Compliance:** Keine automatische Annahme oder Ablehnung. Das Tool bewertet explizit **keine** sensiblen Merkmale (Alter, Geschlecht, Foto, Herkunft, Familienstand) und dient rein als strukturierte Entscheidungshilfe.
- **Robustes Fallback-Scoring:** Fehlt der API-Schlüssel oder ist die KI nicht erreichbar, schaltet das System automatisch in den Fallback-Modus und skaliert die verbleibenden Kriterien präzise auf 100%.
- **Hohe Testabdeckung:** Eine umfassende Test-Suite (30 automatisierte Unit-Tests via `pytest`) validiert das PDF-Parsing, das Keyword-Matching, das Scoring, den Export und die KI-Mocks.

---

## 📋 Funktionsumfang

1. **PDF-Parsing:** Schnelles und robustes Einlesen von PDF-Dokumenten via PyMuPDF.
2. **Kriteriendefinition:** Eingabe von Muss-Kriterien, Wunsch-Kriterien und Keywords direkt in der UI oder durch Laden von Beispieldaten.
3. **Erklärbares Scoring:** Transparente Aufteilung des Scores nach Kriterienerfüllung, Berufserfahrung und KI-Bewertung.
4. **Detaildossier:** Zusammenfassung des Bewerbers, Stärken/Schwächen-Auflistung, Belege direkt aus dem Text und generierte Interviewfragen.
5. **Ergebnisexport:** Einfacher Export des Rankings und der Dossiers als strukturierte JSON- oder lesbare Markdown-Dateien.

---

## ⚙️ Setup & Installation

### Voraussetzungen
- Python 3.9 oder neuer
- Ein OpenRouter-Konto (optional, für KI-Analysen)

### Installation

1. **Repository klonen / in das Projektverzeichnis wechseln:**
   ```bash
   git clone <repo-url>
   cd KI_Bewerbungs_Screening
   ```

2. **Virtuelle Umgebung erstellen und aktivieren:**
   ```bash
   python -m venv .venv
   # Unter Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # Unter macOS/Linux:
   source .venv/bin/activate
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurationsdatei anlegen:**
   Erstellen Sie eine `.env`-Datei im Hauptverzeichnis (Sie können `.env.example` als Vorlage kopieren) und tragen Sie optional Ihren API-Schlüssel ein:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   OPENROUTER_MODEL=moonshotai/kimi-k2.6:free
   ```

5. **Streamlit-Anwendung starten:**
   ```bash
   streamlit run app.py
   ```
   Die App öffnet sich automatisch in Ihrem Browser unter `http://localhost:8501`.

---

## 🚀 Benutzung & Workflow

### 1. Das Demo-Szenario testen
Das Projekt enthält ein vollständig vorbereitetes Demo-Szenario, um den Prototypen sofort auszuprobieren:
- Klicken Sie auf dem **Dashboard** auf **„Demo-Szenario analysieren“**.
- Die App lädt automatisch eine vorgegebene Stellenbeschreibung (Full-Stack-Rolle) und führt die Analyse für **7 synthetische Bewerber-PDFs** aus `sample_data/fake_resumes/` durch.
- Die Test-Bewerber decken verschiedene Qualifikationsstufen und Randfälle ab (vom perfekten Fit über Synonym-Übereinstimmungen bis hin zu einem gescannten PDF ohne lesbaren Text).

### 2. Eigene Bewerbungen analysieren
- Wechseln Sie zum Tab **„Bewerbungen hochladen“**.
- Geben Sie Ihre Anforderungen ein (Muss-Kriterien, Wunsch-Kriterien und Keywords).
- Ziehen Sie eine oder mehrere Lebenslauf-PDFs per Drag-and-Drop in den Uploader.
- Klicken Sie auf **„Bewerbungen analysieren“**.

### 3. KI-Konfiguration & Modelle einstellen
- Unter **„Einstellungen“** können Sie Ihren OpenRouter API-Schlüssel hinterlegen und ein gewünschtes Modell wählen (z. B. das kostenlose `openrouter/owl-alpha`).
- Sie können auch die **Score-Gewichtung** (z. B. wie stark Muss-Kriterien oder die KI-Bewertung gewichtet werden) flexibel anpassen.

---

## 🧪 Tests ausführen

Das Projekt verfügt über automatisierte Tests, um die Korrektheit der Parser, des Matchers und des Scorings zu überprüfen:
```bash
python -m pytest -v
```

---

## 📁 Projektstruktur

```text
├── app.py                     # Streamlit Hauptanwendung, Layout & UI-State
├── config.py                  # API-Konfiguration, Standardmodelle & ScoreWeights
├── pdf_parser.py              # PDF-Extraktion & Textbereinigung via PyMuPDF
├── keyword_matcher.py         # Keyword- und Synonymerkennung im Lebenslauftext
├── scoring.py                 # Berechnungslogik für das regelbasierte Fit-Scoring
├── ai_analyzer.py             # OpenRouter-Schnittstelle & LLM-Prompting
├── ranking.py                 # Hilfsfunktionen zur Kandidatensortierung
├── schemas.py                 # Pydantic-Schemas für strukturierte JSON-Ausgaben
├── export_utils.py            # JSON/Markdown Export-Helper
├── sample_data/               # Beispieldaten & synthetische Profile
│   ├── sample_job_description.txt
│   ├── sample_keywords.json
│   ├── test_outcomes/         # Exportierte Beispiel-Screenings (KI & Fallback)
│   └── fake_resumes/          # Generierte PDF-Testlebensläufe
└── tests/                     # Komplette Test-Suite für alle Kernkomponenten
```

---

## 🔒 Sicherheits- & Datenschutzprinzipien (DSGVO-Compliance)

- **Datenminimierung:** Es findet keine dauerhafte Speicherung von Lebensläufen oder personenbezogenen Daten statt. Alle hochgeladenen Dokumente werden ausschließlich im Arbeitsspeicher der laufenden Streamlit-Session verarbeitet.
- **Gleichbehandlung:** Die Kriterienprüfung erfolgt streng fachlich. Sensible demografische Faktoren wie Alter, Geschlecht, Foto, Herkunft, Religion oder Familienstand werden von der Analyse vollständig ignoriert.
- **Nachvollziehbarkeit:** Jedes Ergebnis enthält eine klare Begründung darüber, wie sich der Score zusammensetzt und welche Belege im Text gefunden wurden.
