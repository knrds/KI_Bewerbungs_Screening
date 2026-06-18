---
name: HR AI Tool Design System
product: AI Resume Screening
language: de
version: 1.0
source_screens:
  - Dashboard / Screening Start / Ranking / Kandidatendetail
  - Einstellungen & KI-Konfiguration
design_goal: Vertrauenswürdiges, ruhiges und strukturiertes HR-SaaS-Interface für KI-gestütztes Resume Screening.
colors:
  background: "#faf8ff"
  surface: "#faf8ff"
  surface-dim: "#d9d9e5"
  surface-bright: "#faf8ff"
  surface-container-lowest: "#ffffff"
  surface-container-low: "#f3f3fe"
  surface-container: "#ededf9"
  surface-container-high: "#e7e7f3"
  surface-container-highest: "#e1e2ed"
  surface-variant: "#e1e2ed"
  surface-tint: "#0053db"
  on-background: "#191b23"
  on-surface: "#191b23"
  on-surface-variant: "#434655"
  outline: "#737686"
  outline-variant: "#c3c6d7"
  primary: "#004ac6"
  primary-container: "#2563eb"
  primary-fixed: "#dbe1ff"
  primary-fixed-dim: "#b4c5ff"
  on-primary: "#ffffff"
  on-primary-container: "#eeefff"
  on-primary-fixed: "#00174b"
  on-primary-fixed-variant: "#003ea8"
  inverse-primary: "#b4c5ff"
  secondary: "#505f76"
  secondary-container: "#d0e1fb"
  secondary-fixed: "#d3e4fe"
  secondary-fixed-dim: "#b7c8e1"
  on-secondary: "#ffffff"
  on-secondary-container: "#54647a"
  on-secondary-fixed: "#0b1c30"
  on-secondary-fixed-variant: "#38485d"
  tertiary: "#943700"
  tertiary-container: "#bc4800"
  tertiary-fixed: "#ffdbcd"
  tertiary-fixed-dim: "#ffb596"
  on-tertiary: "#ffffff"
  on-tertiary-container: "#ffede6"
  on-tertiary-fixed: "#360f00"
  on-tertiary-fixed-variant: "#7d2d00"
  error: "#ba1a1a"
  error-container: "#ffdad6"
  on-error: "#ffffff"
  on-error-container: "#93000a"
  inverse-surface: "#2e3039"
  inverse-on-surface: "#f0f0fb"
semantic_status_colors:
  success:
    background: "#f0fdf4"
    border: "#bbf7d0"
    text: "#15803d"
  warning:
    background: "#fefce8"
    border: "#fde68a"
    text: "#a16207"
  danger:
    background: "#fff1f2"
    border: "#fecdd3"
    text: "#be123c"
  info:
    background: "#eff6ff"
    border: "#bfdbfe"
    text: "#1d4ed8"
typography:
  fontFamily: "Inter"
  headline-lg:
    fontSize: "32px"
    lineHeight: "40px"
    fontWeight: 700
    letterSpacing: "-0.02em"
  headline-lg-mobile:
    fontSize: "24px"
    lineHeight: "32px"
    fontWeight: 700
    letterSpacing: "-0.01em"
  headline-md:
    fontSize: "20px"
    lineHeight: "28px"
    fontWeight: 600
    letterSpacing: "-0.01em"
  body-base:
    fontSize: "16px"
    lineHeight: "24px"
    fontWeight: 400
  body-sm:
    fontSize: "14px"
    lineHeight: "20px"
    fontWeight: 400
  label-md:
    fontSize: "14px"
    lineHeight: "20px"
    fontWeight: 600
  label-sm:
    fontSize: "12px"
    lineHeight: "16px"
    fontWeight: 500
    letterSpacing: "0.05em"
spacing:
  container-max-width: "1440px"
  sidebar-width: "256px"
  topbar-height: "64px"
  margin-desktop: "32px"
  margin-mobile: "16px"
  gutter: "24px"
  stack-sm: "8px"
  stack-md: "16px"
  stack-lg: "24px"
  card-padding: "24px"
radius:
  input: "8px"
  button: "8px"
  chip: "6px"
  card: "12px"
  panel: "12px"
  avatar: "8px"
  full: "9999px"
shadows:
  card: "0 4px 12px rgba(0,0,0,0.04)"
  card-hover: "0 8px 24px rgba(0,0,0,0.06)"
  settings-card: "0 4px 24px rgba(0,0,0,0.04)"
  settings-card-hover: "0 8px 32px rgba(0,0,0,0.06)"
---

# DESIGN.md — HR AI Tool / AI Resume Screening

## 1. Produktidentität

Das Interface gehört zu einem modernen HR-SaaS-Tool für KI-gestütztes Screening von Lebensläufen. Die Anwendung soll Bewerbungen strukturiert voranalysieren, Kandidaten nach Fit Score ranken, Stärken und Schwächen sichtbar machen und Interviewfragen vorbereiten.

Wichtig: Das Design darf nicht wie ein Spielzeug-KI-Demo wirken. Es muss nach einem seriösen internen Unternehmens-Tool aussehen, das HR-Teams bei Entscheidungen unterstützt, aber die Entscheidung nicht automatisiert ersetzt.

**Kernwirkung:**
- vertrauenswürdig
- ruhig
- klar strukturiert
- datenorientiert
- professionell
- schnell erfassbar
- compliance-bewusst

**Design-Motto:**  
> Ruhige Enterprise-Oberfläche mit klarer KI-Unterstützung, starken Prioritäten und wenig visueller Ablenkung.

---

## 2. Designprinzipien

### 2.1 Klarheit vor Effekten
Die Oberfläche soll komplexe Bewerbungsdaten einfach erfassbar machen. Jede Karte, Tabelle und Statusanzeige hat eine klare Funktion. Dekoration wird nur eingesetzt, wenn sie Orientierung verbessert.

### 2.2 Mensch bleibt finaler Entscheider
Die Anwendung darf KI-Bewertungen zeigen, muss aber durch Formulierungen und Compliance-Hinweise klar machen, dass finale Entscheidungen von Menschen getroffen werden.

### 2.3 Priorisierung statt Datenflut
Das wichtigste Ergebnis ist der Kandidaten-Fit. Deshalb werden Score, Status, Muss-Kriterien, fehlende Skills und Interviewfragen visuell höher priorisiert als Rohdaten.

### 2.4 Wiederverwendbare SaaS-Struktur
Navigation, Topbar, Cards, Tabellen, Badges, Inputs und Detailpanels sollen als wiederverwendbare Komponenten angelegt werden.

### 2.5 Ruhige visuelle Hierarchie
Die Farbpalette nutzt sehr helle Oberflächen, dezente Linien und ein kräftiges Blau für aktive Elemente. Dadurch entsteht ein professioneller HR- und Enterprise-Look.

---

## 3. Informationsarchitektur

Die Anwendung besteht aus einem festen App-Shell-Layout:

```text
┌──────────────────────────────────────────────────────────────┐
│ Fixed Sidebar 256px │ Sticky Topbar 64px                     │
│                     ├────────────────────────────────────────┤
│ Navigation          │ Main Canvas                            │
│ User/Role unten     │ Page Content max-width 1440px          │
└──────────────────────────────────────────────────────────────┘
```

### 3.1 Hauptnavigation

Die Sidebar ist dauerhaft sichtbar und enthält:

1. Dashboard
2. Bewerbungen hochladen
3. Ranking
4. Kandidatenanalyse
5. Einstellungen
6. Export

Der aktive Menüpunkt wird durch folgende Kombination markiert:
- Text in `primary`
- Icon in `primary`
- dezente blaue Hintergrundfläche
- rechte 4px Border in `primary`
- optional leicht verkleinerte aktive Darstellung (`scale-[0.98]`)

### 3.2 Topbar

Die Topbar bleibt sticky am oberen Rand. Sie enthält:
- links: Produkt-/Bereichstitel `AI Resume Screening`
- rechts: Modellstatus `OpenRouter Modell`
- rechts: API-Status-Pill `API Status: Aktiv`

Die Topbar nutzt:
- Höhe: `64px`
- Hintergrund: `surface-container-lowest`
- Border Bottom: `outline-variant`
- subtiler Schatten

### 3.3 Main Canvas

Der Hauptbereich beginnt rechts neben der Sidebar:
- `margin-left: 256px`
- Innenabstand Desktop: `32px`
- maximale Content-Breite: `1440px`
- vertikale Abstände: 24px zwischen großen Bereichen

---

## 4. Farbkonzept

Die Palette ist stark an Material-ähnliche Surface-Tokens angelehnt. Sie erzeugt einen hellen, kühlen, professionellen Look.

### 4.1 Hauptfarben

| Token | Wert | Verwendung |
|---|---:|---|
| `primary` | `#004ac6` | primäre Buttons, aktive Icons, Scores, Links |
| `primary-container` | `#2563eb` | stärkere blaue Flächen, Logo/aktive States |
| `background` | `#faf8ff` | App-Hintergrund |
| `surface` | `#faf8ff` | Basisfläche |
| `surface-container-lowest` | `#ffffff` | Cards, Panels, Topbar |
| `surface-container-low` | `#f3f3fe` | dezente Eingabe-/Dropzonenflächen |
| `surface-container` | `#ededf9` | aktive Navigationsflächen, Chips |
| `surface-variant` | `#e1e2ed` | Slider-Tracks, Divider, dezente Flächen |
| `outline-variant` | `#c3c6d7` | Card-Borders, Input-Borders |
| `on-surface` | `#191b23` | Haupttext |
| `on-surface-variant` | `#434655` | Sekundärtext |
| `error` | `#ba1a1a` | Fehler, Warnungen mit Risikocharakter |
| `tertiary` | `#943700` | Highlight für Top-Kandidat/Auszeichnung |

### 4.2 Semantische Farben

Für HR-Status werden klare, aber entsättigte Statusfarben verwendet:

| Status | Background | Border | Text | Beispiel |
|---|---:|---:|---:|---|
| Erfolg | `#f0fdf4` | `#bbf7d0` | `#15803d` | Hohe Priorität, Matched Skills |
| Warnung | `#fefce8` | `#fde68a` | `#a16207` | Manuell prüfen, Fehlend/Schwach |
| Gefahr | `#fff1f2` | `#fecdd3` | `#be123c` | Fehlende Muss-Kriterien |
| Info | `#eff6ff` | `#bfdbfe` | `#1d4ed8` | Modell/API Hinweise |

### 4.3 Farbregeln

- Blau nur für primäre Interaktion, aktive Navigation, Scores und KI-relevante Highlights einsetzen.
- Rot nur für echte Risiken oder Fehler nutzen, nicht für normale negative Werte.
- Warnungen in Gelb/Amber darstellen, wenn manuell geprüft werden soll.
- Große Content-Flächen bleiben weiß oder sehr hell.
- Keine gesättigten Hintergrundflächen über große Bereiche ziehen.

---

## 5. Typografie

Die gesamte Anwendung verwendet ausschließlich **Inter**.

### 5.1 Textstile

| Stil | Größe | Line-height | Gewicht | Einsatz |
|---|---:|---:|---:|---|
| `headline-lg` | 32px | 40px | 700 | Seitentitel, große Kennzahlen |
| `headline-lg-mobile` | 24px | 32px | 700 | Mobile Seitentitel |
| `headline-md` | 20px | 28px | 600 | Card-Titel, Panel-Titel |
| `body-base` | 16px | 24px | 400 | Beschreibungstexte |
| `body-sm` | 14px | 20px | 400 | Tabelleninfos, Hilfetexte |
| `label-md` | 14px | 20px | 600 | Labels, Buttontext, wichtige Kurztexte |
| `label-sm` | 12px | 16px | 500 | Badges, Tabellenheader, Meta-Labels |

### 5.2 Typografie-Regeln

- Seitentitel: `headline-lg`, fett, enger Buchstabenabstand.
- Card-Titel: `headline-md`, semibold.
- Tabellenheader: `label-sm`, uppercase, Tracking.
- Labels über Inputs: `label-md`.
- Hilfetexte unter Inputs: `body-sm`, sekundäre Farbe.
- Zahlen/KPIs: groß und fett, damit sie sofort erfassbar sind.

---

## 6. Layoutsystem

### 6.1 Desktop

- Sidebar: fixed, `256px`
- Topbar: sticky, `64px`
- Main Content: `ml-64`, `p-32px`
- Max Content Width: `1440px`
- Gutter: `24px`

### 6.2 Grid-Regeln

Dashboard:
```text
Metrics:      4 Spalten Desktop / 2 Tablet / 1 Mobile
Upload Card:  2 Spalten Desktop / 1 Mobile
Main Area:    2/3 Ranking Table + 1/3 Kandidatendetail
```

Settings:
```text
Gesamtgrid: 3 Spalten
Links:      1/3 API Settings + Systemlogik
Rechts:     2/3 Score Gewichtung
Mobile:     alles einspaltig
```

### 6.3 Abstände

| Token | Wert | Verwendung |
|---|---:|---|
| `stack-sm` | 8px | Label zu Input, kleine Gruppen |
| `stack-md` | 16px | Elemente innerhalb einer Card |
| `stack-lg` | 24px | Card-Sections, große Blöcke |
| `gutter` | 24px | Grid-Abstand |
| `margin-desktop` | 32px | Main Content Padding |
| `margin-mobile` | 16px | Mobile Padding |

---

## 7. App Shell

### 7.1 Sidebar

**Zweck:** permanente Orientierung und schneller Seitenwechsel.

**Maße:**
- Breite: `256px`
- Höhe: `100vh`
- Position: `fixed left-0 top-0`
- Padding oben/unten: `24px`
- Border rechts: `1px outline-variant`
- Hintergrund: `surface`

**Brand-Block:**
- Icon/Avatar: `40x40px`
- Radius: Dashboard eher `8px`, Settings-Variante teils rund; Standard vereinheitlichen auf `8px`
- Titel: `HR AI Tool`, `headline-md`, primary
- Untertitel: `Modern HR Solutions`, `label-sm`, on-surface-variant

**Navigation Item:**
- Höhe: ca. `40-48px`
- Padding: `12px horizontal`, `8-12px vertical`
- Radius: `8px`
- Icon: `20px`
- Abstand Icon/Text: `12px`

**Aktiver State:**
```css
color: var(--primary);
font-weight: 700;
background: var(--surface-container);
border-right: 4px solid var(--primary);
```

### 7.2 Topbar

**Zweck:** Kontext und Systemstatus.

**Maße:**
- Höhe: `64px`
- Hintergrund: `surface-container-lowest`
- Border Bottom: `outline-variant`
- Sticky oben
- Padding links/rechts: `32px`

**Status-Pills:**
- Radius: full
- Padding: `6px 12px`
- Border: `outline-variant`
- Schrift: `label-sm`
- OpenRouter-Pill: weiß/hell mit blauem Punkt
- API-Status: `secondary-container`, Icon `check_circle`

---

## 8. Seitenstruktur

## 8.1 Dashboard

Das Dashboard ist die Hauptarbeitsfläche zum Starten eines Screenings und zum Prüfen der besten Kandidaten.

### Bereich 1: KPI Cards

Vier Cards in einer Reihe:

1. Analysierte Bewerbungen
   - Wert: `124`
   - Trend Badge: `+12%`
   - Icon: `description`
2. Durchschnittlicher Fit Score
   - Wert: `72%`
   - Icon: `analytics`
3. Top-Kandidat
   - Wert: `Max Mustermann`
   - Icon: `workspace_premium`
4. Fehlende Muss-Kriterien
   - Wert: `12%`
   - Icon: `warning`

**Card-Spezifikation:**
- Hintergrund: `surface-container-lowest`
- Border: `outline-variant`
- Radius: `12px`
- Padding: `24px`
- Shadow: `0 4px 12px rgba(0,0,0,0.04)`
- Hover Shadow: `0 8px 24px rgba(0,0,0,0.06)`

### Bereich 2: Neues Screening starten

Große Card mit Uploadbereich links und Kriterien rechts.

**Upload Dropzone:**
- Border: `2px dashed outline-variant`
- Hintergrund: `surface-container-low`
- Radius: `12px`
- Mindesthöhe: `240px`
- zentraler Upload-Kreis: `64x64px`, primary-container mit geringer Opacity
- Text:
  - Haupttext: `PDF Lebensläufe hier ablegen`
  - Sekundär: `oder klicken um Dateien auszuwählen`

**Kriterienbereich:**
- Textarea: Stellenbeschreibung optional
- Input: Muss-Kriterien
- Input: Wunsch-Kriterien
- Chips für ausgewählte Skills
- Primary Button: `Bewerbungen analysieren`

**Funktionale UX-Regel:**  
Muss-Kriterien müssen visuell wichtiger sein als Wunsch-Kriterien, weil sie im Scoring stärker gewichtet werden und Compliance-/Job-Fit-relevanter sind.

### Bereich 3: Ranking + Kandidatendetail

Desktop-Layout:
- Ranking: `lg:col-span-2`
- Detailpanel: `lg:col-span-1`
- beide ca. `600px` Höhe
- beide scrollbar, falls Inhalt länger wird

#### Ranking Table

Spalten:
- Rang
- Bewerber
- Fit Score
- Status
- Aktion

**Tabellenregeln:**
- Header sticky
- Header uppercase in `label-sm`
- Zeilenhöhe großzügig, ca. `56-72px`
- Hover: `surface-container-low`
- Aktive/ausgewählte Zeile: leichter Primary-Tint (`primary/5`)
- Rang als runder Badge
- Score als Zahl plus Progress Bar
- Aktion über Icon `visibility`

#### Kandidatendetail

Inhalte:
- Name
- Standort
- runder Score-Indikator
- KI-Zusammenfassung
- Matched Skills
- Fehlend / Schwach
- empfohlene Interview-Fragen
- Aktionen: Einladen / Absagen

**UX-Regel:**  
Das Detailpanel soll wie ein Entscheidungs-Dossier wirken. Es muss kompakt genug sein, um schnell geprüft zu werden, aber alle kritischen Informationen enthalten.

### Bereich 4: Compliance Footer

Am unteren Ende:
- Icon `info`
- Text: `Dieses Tool unterstützt nur die strukturierte Voranalyse. Die finale Entscheidung trifft immer ein Mensch entsprechend den Compliance-Richtlinien.`
- Hintergrund: `surface-container-low`
- Border: `outline-variant`
- Radius: `8px`

---

## 8.2 Einstellungen & KI-Konfiguration

Diese Seite dient zur Verwaltung der KI-Anbindung und der Scoring-Logik.

### Page Header

- Titel: `Einstellungen & KI-Konfiguration`
- Beschreibung: `Verwalten Sie hier die API-Zugänge und konfigurieren Sie die Gewichtung für das Kandidaten-Scoring.`
- Titel: `headline-lg`
- Beschreibung: `body-base`, sekundäre Textfarbe

### Layout

Desktop:
- 3-Spalten-Grid
- linke Spalte: API Settings + Systemlogik
- rechte 2 Spalten: Score Gewichtung

Mobile:
- einspaltig
- Score Gewichtung unter API/Systemlogik

### API Settings Card

Inhalte:
- Card Header mit Icon `key`
- OpenRouter API Key als Password Input
- Visibility Toggle Icon
- Modell-ID Input
- Hilfetext: `Standardmodell für KI-Analysen.`

**Sicherheitsregel:**  
API Keys niemals im Klartext anzeigen. Die Sichtbarkeitsfunktion muss bewusst ausgelöst werden.

### Systemlogik Card

Inhalte:
- Toggle `KI-Analyse verwenden`
- Toggle `Fallback-Scoring aktivieren`
- Beschreibungstexte unter jedem Toggle

**Toggle States:**
- aktiv: `primary`, weißer Knob rechts
- inaktiv: `surface-variant`, weißer Knob links mit Border

### Score Gewichtung

Inhalte:
- Header mit Icon `balance`
- Badge `Total: 100%`
- Slider:
  - Muss-Kriterien: 40%
  - Wunsch-Kriterien: 20%
  - Skill Match: 20%
  - Erfahrung: 10%
  - KI-Bewertung / Soft Skills: 10%
- Button `Konfiguration speichern`

**Scoring-Regel:**  
Die Summe muss immer 100% ergeben. Wird ein Slider verändert, muss entweder:
1. die Summe validiert werden und Speichern blockieren, falls nicht 100%, oder
2. das System normalisiert die übrigen Werte automatisch.

Empfohlene UX: Variante 1 ist transparenter für HR-Tools.

**Prioritätslogik:**  
Muss-Kriterien bleiben der stärkste Faktor. Der Nutzer darf sie reduzieren, aber die Default-Konfiguration sollte ihre Bedeutung klar zeigen.

---

## 9. Komponentenbibliothek

## 9.1 Card

**Standard:**
```css
background: #ffffff;
border: 1px solid #c3c6d7;
border-radius: 12px;
padding: 24px;
box-shadow: 0 4px 12px rgba(0,0,0,0.04);
```

**Hover:**
```css
box-shadow: 0 8px 24px rgba(0,0,0,0.06);
```

**Varianten:**
- KPI Card
- Upload Card
- Table Card
- Detail Panel
- Settings Card
- Compliance Card

## 9.2 Button

### Primary Button

Verwendung:
- Bewerbungen analysieren
- Konfiguration speichern
- Einladen

```css
background: #004ac6;
color: #ffffff;
border-radius: 8px;
padding: 10px 24px;
font-size: 14px;
font-weight: 600;
line-height: 20px;
```

Hover:
```css
background: rgba(0, 74, 198, 0.9);
```

### Secondary Button

Verwendung:
- Absagen
- alternative Aktionen

```css
background: transparent;
color: #191b23;
border: 1px solid #c3c6d7;
border-radius: 8px;
padding: 10px 24px;
```

Hover:
```css
background: #ededf9;
```

## 9.3 Input / Textarea

```css
background: #ffffff;
border: 1px solid #c3c6d7;
border-radius: 8px;
padding: 10px 12px;
font-size: 14px;
line-height: 20px;
color: #191b23;
```

Focus:
```css
border-color: #004ac6;
box-shadow: 0 0 0 1px #004ac6;
outline: none;
```

Placeholder:
```css
color: #737686;
```

## 9.4 Chips

Verwendung:
- Skills
- Kriterien
- Status-Metadaten

```css
display: inline-flex;
align-items: center;
gap: 4px;
background: #ededf9;
border: 1px solid #c3c6d7;
border-radius: 6px;
padding: 4px 10px;
font-size: 12px;
line-height: 16px;
```

Skill-Chips können ein `close` Icon enthalten.

## 9.5 Badges / Status

### Hohe Priorität
- Background: `#f0fdf4`
- Border: `#bbf7d0`
- Text: `#15803d`

### Geeignet
- Background: `surface-container`
- Border: `outline-variant`
- Text: `on-surface-variant`

### Manuell prüfen
- Background: `#fefce8`
- Border: `#fde68a`
- Text: `#a16207`

### API Status Aktiv
- Background: `secondary-container`
- Text: `on-secondary-container`
- Icon: `check_circle`

## 9.6 Progress Bar

Verwendung:
- Fit Score in Ranking Table

```css
track:
  height: 8px;
  background: #e1e2ed;
  border-radius: 9999px;

fill:
  background: #004ac6;
  border-radius: 9999px;
```

Score über 85%:
- primary oder primary/70

Score 60-84%:
- secondary oder abgeschwächtes Blau/Grau

Score unter 60%:
- warning oder muted, nicht automatisch rot

## 9.7 Slider

Verwendung:
- Score Gewichtung

```css
height: 8px;
track: #e1e2ed;
thumb/accent: #004ac6;
border-radius: 9999px;
```

Slider-Werte rechts als `label-md` in primary darstellen.

## 9.8 Toggle

Aktiv:
```css
track: #004ac6;
knob: #ffffff;
knob-position: right;
```

Inaktiv:
```css
track: #e1e2ed;
knob: #ffffff;
knob-border: #c3c6d7;
knob-position: left;
```

## 9.9 Tables

```css
table:
  width: 100%;
  border-collapse: collapse;

thead:
  position: sticky;
  top: 0;
  background: #ffffff;
  border-bottom: 1px solid #c3c6d7;

th:
  font-size: 12px;
  line-height: 16px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #434655;

td:
  padding: 12px 16px;
```

---

## 10. Icons

Es werden **Material Symbols Outlined** verwendet.

### Standard-Icons

| Bereich | Icon |
|---|---|
| Logo / KI | `psychology` |
| Dashboard | `dashboard` |
| Upload | `upload_file`, `cloud_upload` |
| Ranking | `format_list_numbered` |
| Analyse | `analytics` |
| Einstellungen | `settings` |
| Export | `ios_share` |
| API Key | `key` |
| Systemlogik | `tune` |
| Score Gewichtung | `balance` |
| Speichern | `save` |
| Sichtbarkeit | `visibility`, `visibility_off` |
| Kandidat ansehen | `visibility` |
| Status aktiv | `check_circle` |
| Warnung | `warning` |
| Info | `info` |
| Start Analyse | `play_arrow` |

### Icon-Regeln

- Navigation Icons: 20px
- KPI Icons: 24px in 40x40px Icon-Container
- Upload Icon: 32px in 64x64px Kreis
- Inline Icons: 14-18px
- Icons immer semantisch einsetzen, nicht dekorativ überladen

---

## 11. Interaktionen und States

### 11.1 Hover
- Cards: Schatten leicht erhöhen
- Navigation Items: Hintergrund `surface-container`
- Tabellenzeilen: Hintergrund `surface-container-low`
- Buttons: Primary leicht abdunkeln, Secondary mit Surface-Hintergrund

### 11.2 Focus
Alle interaktiven Elemente brauchen sichtbaren Focus State:
```css
outline: none;
border-color: #004ac6;
box-shadow: 0 0 0 1px #004ac6;
```

### 11.3 Disabled
```css
opacity: 0.5;
cursor: not-allowed;
```

### 11.4 Loading
Für KI-Analyse:
- Button zeigt Spinner oder `Analysiere...`
- Upload Card wird gesperrt
- Ranking kann Skeleton Rows anzeigen
- Status-Pill kann `KI-Analyse läuft` anzeigen

### 11.5 Empty States
Wenn noch keine Bewerbung analysiert wurde:
- Ranking Table zeigt leeren State mit Upload-Hinweis
- Detailpanel zeigt Platzhalter: `Wählen Sie einen Kandidaten aus`
- KPIs zeigen `0` oder `–`

### 11.6 Error States
Bei API-Fehler:
- API-Status-Pill wird rot/amber
- Text: `API Status: Fehler` oder `Fallback aktiv`
- Falls Fallback aktiviert: Hinweis, dass Keyword-Matching genutzt wurde
- Kein stilles Fehlschlagen

---

## 12. UX-Regeln für KI und HR-Compliance

### 12.1 KI-Bewertungen erklären
Jeder Score sollte mindestens eine kurze Begründung haben:
- gematchte Skills
- fehlende Muss-Kriterien
- Erfahrung
- Soft-Skill-Indikatoren
- konkrete Textstellen aus dem Lebenslauf, sofern verfügbar

### 12.2 Keine absolute Wahrheit suggerieren
Nicht schreiben:
- `Bester Kandidat`
- `Automatisch einstellen`
- `Ungeeignet`

Besser:
- `Top-Kandidat`
- `Hohe Priorität`
- `Manuell prüfen`
- `Fehlend / Schwach`

### 12.3 Muss-Kriterien sichtbar machen
Fehlende Muss-Kriterien müssen klar markiert werden, weil sie die Entscheidung stark beeinflussen.

### 12.4 Interviewfragen konkret halten
Interviewfragen sollten sich auf erkannte Skills und Lücken beziehen. Beispiel:
- React-Erfahrung vertiefen
- Docker-Grundlagen prüfen
- CI/CD Setup besprechen

---

## 13. Responsive Verhalten

### Desktop ab 1024px
- Sidebar bleibt fixed
- Topbar sticky
- Dashboard nutzt 4 KPI-Spalten
- Ranking und Detailpanel nebeneinander
- Settings nutzt 1/3 + 2/3 Layout

### Tablet
- KPI Cards: 2 Spalten
- Upload/Kriterien ggf. 1 oder 2 Spalten je nach Breite
- Ranking und Detailpanel können untereinander fallen

### Mobile
- Sidebar sollte zu Drawer oder Bottom Navigation werden
- Content Padding: `16px`
- Alle Grids einspaltig
- Tabellen müssen horizontal scrollen oder als Cards dargestellt werden
- Detailpanel unter Ranking anzeigen
- Seitentitel nutzt `headline-lg-mobile`

---

## 14. Implementierungsrichtlinien mit Tailwind

### 14.1 Tailwind Theme Tokens

Die Tailwind-Konfiguration soll die Design Tokens direkt abbilden:

```js
theme: {
  extend: {
    colors: {
      primary: "#004ac6",
      "primary-container": "#2563eb",
      background: "#faf8ff",
      surface: "#faf8ff",
      "surface-container-lowest": "#ffffff",
      "surface-container-low": "#f3f3fe",
      "surface-container": "#ededf9",
      "surface-variant": "#e1e2ed",
      "outline-variant": "#c3c6d7",
      "on-surface": "#191b23",
      "on-surface-variant": "#434655",
      error: "#ba1a1a"
    },
    spacing: {
      "container-max-width": "1440px",
      "margin-desktop": "32px",
      "margin-mobile": "16px",
      "gutter": "24px",
      "stack-sm": "8px",
      "stack-md": "16px",
      "stack-lg": "24px"
    },
    fontFamily: {
      "body-base": ["Inter"],
      "body-sm": ["Inter"],
      "headline-lg": ["Inter"],
      "headline-md": ["Inter"],
      "label-md": ["Inter"],
      "label-sm": ["Inter"]
    }
  }
}
```

### 14.2 Wiederverwendbare Klassen

**App Card:**
```html
<div class="bg-surface-container-lowest rounded-xl border border-outline-variant p-6 shadow-[0_4px_12px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_24px_rgba(0,0,0,0.06)] transition-shadow">
```

**Primary Button:**
```html
<button class="bg-primary hover:bg-primary/90 text-on-primary font-label-md text-label-md px-6 py-2.5 rounded-lg flex items-center gap-2 transition-colors">
```

**Input:**
```html
<input class="w-full rounded-lg border-outline-variant bg-surface-container-lowest focus:border-primary focus:ring-1 focus:ring-primary text-body-sm p-2.5">
```

**Status Badge:**
```html
<span class="inline-flex items-center px-2 py-1 rounded-md font-label-sm text-label-sm border">
```

---

## 15. Qualitätscheckliste

Vor jeder neuen UI-Seite prüfen:

- Nutzt die Seite die gleiche Sidebar und Topbar?
- Ist der Main Content maximal 1440px breit?
- Sind alle Cards weiß mit subtiler Border und weichem Schatten?
- Sind primäre Aktionen klar blau?
- Sind Statusfarben semantisch korrekt?
- Ist der KI-Score immer begründet?
- Gibt es einen klaren Empty State?
- Gibt es sichtbare Loading- und Error-States?
- Ist die Summe der Score-Gewichtung 100%?
- Bleibt die finale HR-Entscheidung beim Menschen?
- Sind Inputs, Buttons und Tabellen konsistent?
- Funktioniert das Layout auch mobil einspaltig?

---

## 16. Konkrete Seiten-Spezifikation

### Dashboard Route: `/dashboard`

**Ziel:** Übersicht über Screening-Ergebnisse und schneller Start neuer Analysen.

**Module:**
1. KPI Row
2. Screening Start Card
3. Ranking Table
4. Candidate Detail Panel
5. Compliance Footer

**Primäre Aktion:** `Bewerbungen analysieren`

**Sekundäre Aktionen:** Kandidat ansehen, Filter öffnen, Einladen, Absagen

---

### Upload Route: `/upload`

**Ziel:** PDFs sammeln und Job-Kriterien definieren.

**Module:**
1. Große Dropzone
2. Stellenbeschreibung
3. Muss-Kriterien
4. Wunsch-Kriterien
5. Upload-Liste mit Status
6. Analyse starten

**Hinweis:** Diese Route kann funktional aus der Dashboard-Upload-Card erweitert werden.

---

### Ranking Route: `/ranking`

**Ziel:** Kandidaten vergleichen und priorisieren.

**Module:**
1. Filterbar/Suchbare Ranking Table
2. Score-Facetten
3. Status-Badges
4. Kandidat öffnen
5. Export/Shortlist

---

### Kandidatenanalyse Route: `/candidates/:id`

**Ziel:** Detaillierte KI-Analyse eines einzelnen Kandidaten.

**Module:**
1. Kandidatenkopf mit Score
2. Zusammenfassung
3. Skill Match
4. fehlende Muss-Kriterien
5. Erfahrung
6. Soft-Skill-Bewertung
7. Interviewfragen
8. Entscheidungsnotizen

---

### Einstellungen Route: `/settings`

**Ziel:** API, Modell und Scoring-Logik konfigurieren.

**Module:**
1. API Settings
2. Systemlogik
3. Score Gewichtung
4. Speichern/Validierung
5. API-Test optional

**Primäre Aktion:** `Konfiguration speichern`

---

### Export Route: `/export`

**Ziel:** Ergebnisse für HR-Prozesse nutzbar machen.

**Module:**
1. Export-Format wählen
2. Kandidaten auswählen
3. Datenschutz-/Compliance-Hinweis
4. Export starten

**Mögliche Formate:** CSV, PDF Report, JSON, Shortlist.

---

## 17. Empfohlene technische Struktur

```text
src/
  components/
    layout/
      AppShell.tsx
      Sidebar.tsx
      Topbar.tsx
    ui/
      Card.tsx
      Button.tsx
      Input.tsx
      Textarea.tsx
      Badge.tsx
      Toggle.tsx
      Slider.tsx
      ProgressBar.tsx
      DataTable.tsx
      EmptyState.tsx
      LoadingState.tsx
    screening/
      UploadDropzone.tsx
      CriteriaInput.tsx
      CandidateRankingTable.tsx
      CandidateDetailPanel.tsx
      ScoreWeightingForm.tsx
      ApiSettingsForm.tsx
  pages/
    Dashboard.tsx
    Upload.tsx
    Ranking.tsx
    CandidateAnalysis.tsx
    Settings.tsx
    Export.tsx
  styles/
    tokens.css
    globals.css
```

---

## 18. Zusammenfassung

Das Designsystem für das HR AI Tool basiert auf einem hellen Enterprise-SaaS-Look mit klarer App-Shell, festem Navigationssystem, ruhigen Card-Flächen und präzisen Statusanzeigen. Der zentrale visuelle Fokus liegt auf Kandidaten-Fit, Muss-Kriterien, KI-Zusammenfassung und Interviewvorbereitung.

Die Anwendung soll professionell genug für HR-Prozesse wirken, aber gleichzeitig einfach genug bleiben, damit der Nutzer Screening-Ergebnisse schnell versteht und sinnvoll weiterverarbeiten kann.
