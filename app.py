from __future__ import annotations

import json
import runpy
from pathlib import Path
from typing import Iterable

import streamlit as st

from ai_analyzer import analyze_resume_with_ai, build_fallback_ai_analysis
from config import (
    DEFAULT_MODEL,
    HUMAN_REVIEW_NOTICE,
    MODEL_OPTIONS,
    ScoreWeights,
    get_openrouter_api_key,
    resolve_model_choice,
)
from export_utils import export_json, export_markdown
from keyword_matcher import match_candidate_text, split_terms
from pdf_parser import extract_text_from_pdf
from ranking import sort_candidates
from schemas import AIAnalysis, CandidateEvaluation, InterviewQuestions
from scoring import calculate_rule_based_score


DEMO_RESUME_FILES = [
    Path("sample_data/fake_resumes/max_mustermann.pdf"),
    Path("sample_data/fake_resumes/erika_musterfrau.pdf"),
    Path("sample_data/fake_resumes/john_doe.pdf"),
    Path("sample_data/fake_resumes/lea_synonym_match.pdf"),
    Path("sample_data/fake_resumes/otto_manager_profile.pdf"),
    Path("sample_data/fake_resumes/nina_data_analyst.pdf"),
    Path("sample_data/fake_resumes/scan_ohne_text.pdf"),
]

PAGES = [
    "Dashboard",
    "Bewerbungen hochladen",
    "Ranking",
    "Kandidatenanalyse",
    "Einstellungen",
    "Export",
]


@st.dialog("Schnellanleitung")
def show_intro_dialog() -> None:
    st.markdown(
        """
        Dieses Tool unterstützt die strukturierte Voranalyse von Bewerbungen.

        1. Kriterien und Keywords definieren.
        2. PDF-Lebensläufe hochladen.
        3. Analyse starten.
        4. Ranking, Begründungen und Interviewfragen prüfen.

        Ohne OpenRouter API-Key bleibt die App im regelbasierten Fallback-Modus
        nutzbar.
        """
    )
    if st.button("Verstanden", type="primary", use_container_width=True):
        st.session_state["seen_intro"] = True
        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="AI Resume Screening",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_design_css()
    init_session_state()
    apply_pending_navigation()

    if not st.session_state["seen_intro"]:
        show_intro_dialog()

    render_sidebar()
    settings = get_runtime_settings()
    render_topbar(settings)

    active_page = st.session_state["active_page"]
    if active_page == "Dashboard":
        render_dashboard(settings)
    elif active_page == "Bewerbungen hochladen":
        render_upload_page(settings)
    elif active_page == "Ranking":
        render_ranking_page()
    elif active_page == "Kandidatenanalyse":
        render_candidate_analysis_page()
    elif active_page == "Einstellungen":
        render_settings_page(settings)
    elif active_page == "Export":
        render_export_page()

    render_compliance_footer()


def sync_persistent_state() -> None:
    if "persistent_storage" not in st.session_state:
        st.session_state["persistent_storage"] = {
            "job_desc": "",
            "must_have": "",
            "nice_to_have": "",
            "keywords": "",
            "use_ai": True,
            "fallback_enabled": True,
            "api_key_input": "",
            "model_choice": DEFAULT_MODEL,
            "custom_model_choice": "",
            "ranking_search": "",
            "ranking_status_filter": "Alle Status",
            "ranking_min_score": 0,
            "show_api_key": False,
        }

    storage = st.session_state["persistent_storage"]

    # Copy current widget values if they exist in session state to persistent storage
    for key in storage:
        if key in st.session_state:
            storage[key] = st.session_state[key]

    # Populate session state with persistent values
    for key, val in storage.items():
        st.session_state[key] = val


def init_session_state() -> None:
    defaults = {
        "active_page": "Dashboard",
        "pending_page": None,
        "seen_intro": False,
        "job_desc": "",
        "must_have": "",
        "nice_to_have": "",
        "keywords": "",
        "evaluations": [],
        "selected_candidate_id": None,
        "analysis_errors": [],
        "last_fallback_active": False,
        "last_analysis_mode": "Noch keine Analyse",
        "use_ai": True,
        "fallback_enabled": True,
        "api_key_input": "",
        "model_choice": DEFAULT_MODEL,
        "custom_model_choice": "",
        "settings_saved_message": "",
        "show_api_key": False,
        "score_weights": {
            "must_have": 40,
            "nice_to_have": 20,
            "skills": 20,
            "seniority": 10,
            "ai_semantic": 10,
        },
        "review_actions": {},
        "ranking_search": "",
        "ranking_status_filter": "Alle Status",
        "ranking_min_score": 0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    sync_persistent_state()



def apply_pending_navigation() -> None:
    pending_page = st.session_state.get("pending_page")
    if pending_page in PAGES:
        st.session_state["active_page"] = pending_page
    st.session_state["pending_page"] = None


def navigate_to(page: str) -> None:
    if page not in PAGES:
        return
    st.session_state["pending_page"] = page


def inject_design_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700&display=swap');

        :root {
            --background: #faf8ff;
            --surface: #faf8ff;
            --surface-lowest: #ffffff;
            --surface-low: #f3f3fe;
            --surface-container: #ededf9;
            --surface-variant: #e1e2ed;
            --outline-variant: #c3c6d7;
            --outline: #737686;
            --primary: #004ac6;
            --primary-container: #2563eb;
            --secondary-container: #d0e1fb;
            --on-surface: #191b23;
            --on-surface-variant: #434655;
            --input-bg: #ffffff;
            --input-placeholder: #737686;
            --shadow-card: 0 4px 12px rgba(0,0,0,0.04);
            --error: #ba1a1a;
            --success-bg: #f0fdf4;
            --success-border: #bbf7d0;
            --success-text: #15803d;
            --warning-bg: #fefce8;
            --warning-border: #fde68a;
            --warning-text: #a16207;
            --danger-bg: #fff1f2;
            --danger-border: #fecdd3;
            --danger-text: #be123c;
            --info-bg: #eff6ff;
            --info-border: #bfdbfe;
            --info-text: #1d4ed8;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --background: #11131a;
                --surface: #151821;
                --surface-lowest: #1c202b;
                --surface-low: #222736;
                --surface-container: #2a3040;
                --surface-variant: #3a4154;
                --outline-variant: #4b5568;
                --outline: #8a93a6;
                --primary: #8fb1ff;
                --primary-container: #2563eb;
                --secondary-container: #253244;
                --on-surface: #f3f6ff;
                --on-surface-variant: #c4cada;
                --input-bg: #1c202b;
                --input-placeholder: #a8afc0;
                --shadow-card: 0 8px 24px rgba(0,0,0,0.28);
                --success-bg: #0f2a1b;
                --success-border: #1f6b3a;
                --success-text: #86efac;
                --warning-bg: #30260a;
                --warning-border: #8a650d;
                --warning-text: #facc15;
                --danger-bg: #34151b;
                --danger-border: #7f1d2d;
                --danger-text: #fda4af;
                --info-bg: #14233d;
                --info-border: #284b85;
                --info-text: #93c5fd;
            }
        }

        html, body, .stApp {
            background: var(--background) !important;
            color: var(--on-surface) !important;
            font-family: Inter, sans-serif;
            color-scheme: light dark;
            --primary-color: var(--primary-container) !important;
            --primary-color-hover: var(--primary) !important;
            --primary-color-active: var(--primary) !important;
            --text-color: var(--on-surface) !important;
            --background-color: var(--background) !important;
            --secondary-background-color: var(--surface-low) !important;
            --border-color: var(--outline-variant) !important;
            --slider-color: var(--primary-container) !important;
        }

        header,
        footer,
        #MainMenu,
        .stDeployButton,
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stDeployButton"],
        [data-testid="stAppDeployButton"],
        [data-testid="stMainMenu"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        button[title="Close sidebar"],
        button[title="Hide sidebar"],
        button[aria-label="Close sidebar"],
        button[aria-label="Hide sidebar"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
        }

        [data-testid="stSidebar"] {
            background: var(--surface) !important;
            border-right: 1px solid var(--outline-variant) !important;
            box-shadow: var(--shadow-card);
        }

        [data-testid="stSidebar"] * {
            font-family: Inter, sans-serif;
            color: var(--on-surface);
        }

        [data-testid="stSidebar"] [role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            width: 100%;
            min-height: 40px;
            border-radius: 8px;
            padding: 8px 12px !important;
            background: transparent !important;
            color: var(--on-surface-variant) !important;
            border: 1px solid transparent !important;
            cursor: pointer;
            transition: background 120ms ease, color 120ms ease, border 120ms ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: var(--surface-container) !important;
            color: var(--on-surface) !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: var(--surface-container) !important;
            color: var(--primary) !important;
            border-color: var(--outline-variant) !important;
            box-shadow: inset -4px 0 0 var(--primary);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label p,
        [data-testid="stSidebar"] [role="radiogroup"] label span {
            color: inherit !important;
            font-weight: 700;
            font-size: 14px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child,
        [data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child {
            display: none !important;
            width: 0 !important;
            min-width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] input[type="radio"] {
            opacity: 0 !important;
            width: 0 !important;
            min-width: 0 !important;
            margin: 0 !important;
            position: absolute !important;
        }

        .block-container {
            max-width: 1440px;
            padding-top: 1.25rem !important;
            padding-bottom: 2.5rem;
        }

        .app-topbar {
            position: sticky;
            top: 0;
            z-index: 20;
            background: color-mix(in srgb, var(--surface-lowest) 96%, transparent);
            border: 1px solid var(--outline-variant);
            border-radius: 12px;
            box-shadow: var(--shadow-card);
            padding: 14px 18px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .topbar-title {
            font-size: 20px;
            line-height: 28px;
            font-weight: 700;
            color: var(--on-surface);
        }

        .topbar-pills {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border-radius: 9999px;
            border: 1px solid var(--outline-variant);
            padding: 6px 12px;
            font-size: 12px;
            line-height: 16px;
            font-weight: 600;
            color: var(--on-surface-variant);
            background: var(--surface-lowest);
        }

        .pill-info {
            background: var(--info-bg);
            border-color: var(--info-border);
            color: var(--info-text);
        }

        .pill-success {
            background: var(--success-bg);
            border-color: var(--success-border);
            color: var(--success-text);
        }

        .pill-warning {
            background: var(--warning-bg);
            border-color: var(--warning-border);
            color: var(--warning-text);
        }

        .dot {
            width: 8px;
            height: 8px;
            border-radius: 9999px;
            background: currentColor;
            display: inline-block;
        }

        .page-title {
            font-size: 32px;
            line-height: 40px;
            font-weight: 700;
            letter-spacing: 0;
            margin: 0 0 6px;
            color: var(--on-surface);
        }

        .page-subtitle {
            font-size: 16px;
            line-height: 24px;
            color: var(--on-surface-variant);
            margin: 0 0 24px;
        }

        .app-card {
            background: var(--surface-lowest);
            border: 1px solid var(--outline-variant);
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--shadow-card);
            margin-bottom: 24px;
        }

        .app-card-tight {
            background: var(--surface-lowest);
            border: 1px solid var(--outline-variant);
            border-radius: 12px;
            padding: 18px;
            box-shadow: var(--shadow-card);
            margin-bottom: 16px;
        }

        .section-spacer {
            height: 24px;
        }

        .section-spacer-sm {
            height: 16px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            margin-bottom: 24px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 20px 20px 22px;
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 20px;
            line-height: 28px;
            font-weight: 700;
            color: var(--on-surface);
            margin: 0 0 16px;
        }

        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined';
            font-weight: normal;
            font-style: normal;
            font-size: 20px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
        }

        .kpi-card {
            background: var(--surface-lowest);
            border: 1px solid var(--outline-variant);
            border-radius: 12px;
            padding: 22px;
            box-shadow: var(--shadow-card);
            min-height: 150px;
        }

        .kpi-icon {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            background: #dbe1ff;
            margin-bottom: 16px;
        }

        .kpi-title {
            font-size: 12px;
            line-height: 16px;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--on-surface-variant);
            margin-bottom: 6px;
        }

        .kpi-value {
            font-size: 30px;
            line-height: 36px;
            font-weight: 700;
            color: var(--on-surface);
            word-break: break-word;
        }

        .upload-shell {
            min-height: 240px;
            border: 2px dashed var(--outline-variant);
            border-radius: 12px;
            background: var(--surface-low);
            padding: 22px;
        }

        .upload-hint {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            text-align: center;
            min-height: 112px;
            color: var(--on-surface-variant);
        }

        .upload-circle {
            width: 64px;
            height: 64px;
            border-radius: 9999px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #dbe1ff;
            color: var(--primary);
            margin-bottom: 10px;
        }

        .chip, .chip-success, .chip-warning, .chip-danger, .chip-info {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 12px;
            line-height: 16px;
            font-weight: 600;
            margin: 3px 4px 3px 0;
            border: 1px solid var(--outline-variant);
            background: var(--surface-container);
            color: var(--on-surface-variant);
        }

        .chip-success {
            background: var(--success-bg);
            border-color: var(--success-border);
            color: var(--success-text);
        }

        .chip-warning {
            background: var(--warning-bg);
            border-color: var(--warning-border);
            color: var(--warning-text);
        }

        .chip-danger {
            background: var(--danger-bg);
            border-color: var(--danger-border);
            color: var(--danger-text);
        }

        .chip-info {
            background: var(--info-bg);
            border-color: var(--info-border);
            color: var(--info-text);
        }

        .ranking-header, .ranking-row {
            display: grid;
            grid-template-columns: 58px minmax(180px, 1.5fr) minmax(150px, 1fr) 170px 112px;
            gap: 12px;
            align-items: center;
        }

        .ranking-header {
            color: var(--on-surface-variant);
            font-size: 12px;
            line-height: 16px;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            border-bottom: 1px solid var(--outline-variant);
            padding: 0 0 12px;
            margin-bottom: 4px;
        }

        .ranking-row {
            border-bottom: 1px solid rgba(195,198,215,0.6);
            padding: 12px 0;
        }

        .rank-badge {
            width: 34px;
            height: 34px;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--surface-container);
            color: var(--on-surface-variant);
            font-weight: 700;
        }

        .candidate-name {
            font-size: 14px;
            line-height: 20px;
            font-weight: 700;
            color: var(--on-surface);
        }

        .candidate-meta {
            font-size: 13px;
            line-height: 18px;
            color: var(--on-surface-variant);
        }

        .score-line {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .score-value {
            min-width: 48px;
            font-weight: 700;
            color: var(--primary);
        }

        .score-track {
            width: 100%;
            height: 8px;
            border-radius: 9999px;
            overflow: hidden;
            background: var(--surface-variant);
        }

        .score-fill {
            height: 100%;
            border-radius: 9999px;
            background: var(--primary);
        }

        .status-badge {
            display: inline-flex;
            width: fit-content;
            align-items: center;
            border-radius: 6px;
            border: 1px solid var(--outline-variant);
            padding: 5px 9px;
            font-size: 12px;
            line-height: 16px;
            font-weight: 700;
        }

        .status-high {
            background: var(--success-bg);
            border-color: var(--success-border);
            color: var(--success-text);
        }

        .status-good {
            background: var(--info-bg);
            border-color: var(--info-border);
            color: var(--info-text);
        }

        .status-review {
            background: var(--warning-bg);
            border-color: var(--warning-border);
            color: var(--warning-text);
        }

        .status-low {
            background: var(--surface-container);
            border-color: var(--outline-variant);
            color: var(--on-surface-variant);
        }

        .detail-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 14px;
            margin-bottom: 18px;
        }

        .score-circle {
            width: 56px;
            height: 56px;
            border-radius: 9999px;
            border: 3px solid var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            font-weight: 700;
            font-size: 18px;
            background: var(--surface-lowest);
            flex: 0 0 auto;
        }

        .empty-state {
            border: 1px dashed var(--outline-variant);
            border-radius: 12px;
            background: var(--surface-low);
            color: var(--on-surface-variant);
            padding: 28px;
            margin: 8px 0 14px;
            min-height: 84px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        .demo-hero {
            background: var(--surface-lowest);
            border: 1px solid var(--outline-variant);
            border-radius: 12px;
            box-shadow: var(--shadow-card);
            padding: 24px;
            margin: 24px 0;
        }

        .demo-title {
            font-size: 20px;
            line-height: 28px;
            font-weight: 700;
            color: var(--on-surface);
            margin-bottom: 8px;
        }

        .demo-copy {
            color: var(--on-surface-variant);
            font-size: 14px;
            line-height: 20px;
            margin-bottom: 14px;
        }

        .flow-step {
            border: 1px solid var(--outline-variant);
            border-radius: 8px;
            background: var(--surface-low);
            padding: 12px;
            min-height: 88px;
            margin-bottom: 14px;
        }

        .flow-step strong {
            display: block;
            color: var(--on-surface);
            margin-bottom: 4px;
            font-size: 14px;
        }

        .flow-step span {
            color: var(--on-surface-variant);
            font-size: 13px;
            line-height: 18px;
        }

        .compliance-footer {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            background: var(--surface-low);
            border: 1px solid var(--outline-variant);
            border-radius: 8px;
            padding: 14px 16px;
            color: var(--on-surface-variant);
            font-size: 14px;
            line-height: 20px;
            margin-top: 24px;
        }

        button,
        div[data-testid="stButton"] > button,
        div[data-testid="stDownloadButton"] > button,
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="baseButton-secondary"] {
            border-radius: 8px !important;
            font-weight: 700 !important;
            border: 1px solid var(--outline-variant) !important;
            background: var(--surface-lowest) !important;
            color: var(--on-surface) !important;
            box-shadow: none !important;
        }

        button:hover,
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stDownloadButton"] > button:hover {
            background: var(--surface-container) !important;
            color: var(--on-surface) !important;
            border-color: var(--primary) !important;
        }

        div[data-testid="stButton"] > button[kind="primary"],
        button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        button[data-testid="baseButton-primary"] {
            background: var(--primary-container) !important;
            border-color: var(--primary-container) !important;
            color: #ffffff !important;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover,
        button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        button[data-testid="baseButton-primary"]:hover {
            background: var(--primary) !important;
            border-color: var(--primary) !important;
            color: #ffffff !important;
        }

        button:disabled,
        button[disabled],
        div[data-testid="stButton"] > button:disabled,
        div[data-testid="stDownloadButton"] > button:disabled {
            background: var(--surface-container) !important;
            border-color: var(--outline-variant) !important;
            color: var(--outline) !important;
            opacity: 0.75 !important;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
        div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
            border-radius: 8px !important;
            background: var(--input-bg) !important;
            color: var(--on-surface) !important;
            border-color: var(--outline-variant) !important;
            caret-color: var(--primary) !important;
            box-shadow: none !important;
        }

        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder {
            color: var(--input-placeholder) !important;
            opacity: 1 !important;
        }

        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus,
        div[data-testid="stNumberInput"] input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 1px var(--primary) !important;
        }

        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploaderDropzone"] {
            background: var(--surface-low) !important;
            color: var(--on-surface) !important;
            border: 1px dashed var(--outline-variant) !important;
            border-radius: 12px !important;
        }

        [data-testid="stFileUploader"] section button,
        [data-testid="stFileUploaderDropzone"] button {
            background: var(--surface-lowest) !important;
            color: var(--on-surface) !important;
            border: 1px solid var(--outline-variant) !important;
        }

        [data-testid="stFileUploader"] section small,
        [data-testid="stFileUploader"] section span,
        [data-testid="stFileUploader"] section p {
            color: var(--on-surface-variant) !important;
        }

        [data-testid="stAlert"],
        [data-testid="stNotification"],
        [data-testid="stToast"] {
            color: var(--on-surface) !important;
        }

        input[type="range"],
        [data-testid="stSlider"] input {
            accent-color: var(--primary-container) !important;
        }

        [data-testid="stSlider"] [role="slider"] {
            background: var(--primary-container) !important;
            border-color: var(--primary-container) !important;
            color: var(--primary-container) !important;
        }

        [data-testid="stSlider"] [data-testid="stSliderThumbValue"] p {
            color: var(--primary-container) !important;
        }

        [data-testid="stSlider"] [data-baseweb="slider"] div[style*="height: 0.25rem"] {
            filter: hue-rotate(218deg) saturate(2.1) brightness(0.82) !important;
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span {
            color: inherit;
        }

        @media (max-width: 900px) {
            .app-topbar {
                align-items: flex-start;
                flex-direction: column;
            }
            .topbar-pills {
                justify-content: flex-start;
            }
            .ranking-header {
                display: none;
            }
            .ranking-row {
                grid-template-columns: 42px 1fr;
                gap: 10px;
            }
            .ranking-row > div:nth-child(n+3) {
                grid-column: 2 / -1;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.sidebar.markdown(
        """
        <div style="display:flex;gap:12px;align-items:center;margin:8px 0 24px;">
            <div style="width:40px;height:40px;border-radius:8px;background:#2563eb;color:white;display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined">psychology</span>
            </div>
            <div>
                <div style="font-size:20px;font-weight:700;color:var(--primary);line-height:24px;">HR AI Tool</div>
                <div style="font-size:12px;color:var(--on-surface-variant);line-height:16px;">Modern HR Solutions</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.radio(
        "Navigation",
        PAGES,
        key="active_page",
        label_visibility="collapsed",
    )
    st.sidebar.divider()
    if st.sidebar.button("Schnellanleitung öffnen", use_container_width=True):
        st.session_state["seen_intro"] = False
        st.rerun()
    st.sidebar.caption("Rolle: HR Review")


def get_runtime_settings() -> dict:
    selected_model = resolve_model_choice(
        model_choice=st.session_state.get("model_choice", DEFAULT_MODEL),
        custom_model_choice=st.session_state.get("custom_model_choice", ""),
    )

    api_key = get_openrouter_api_key(st.session_state.get("api_key_input", ""))
    weights_dict = st.session_state["score_weights"]
    weights = ScoreWeights(**weights_dict)

    return {
        "api_key": api_key,
        "api_active": bool(api_key),
        "selected_model": selected_model,
        "use_ai": bool(st.session_state["use_ai"]),
        "fallback_enabled": bool(st.session_state["fallback_enabled"]),
        "weights": weights,
    }


def render_topbar(settings: dict) -> None:
    if settings["use_ai"] and settings["api_active"]:
        model_label = f"🤖 Modell: {settings['selected_model']}"
    else:
        model_label = "🤖 Kein KI-Modell aktiv"

    if settings["api_active"]:
        api_label = "🔑 OpenRouter: Aktiv"
        api_class = "pill-success"
    else:
        api_label = "🔑 OpenRouter: Nicht konfiguriert"
        api_class = "pill-warning"

    if settings["use_ai"] and settings["api_active"]:
        ai_label = "⚙️ Modus: KI-gestützt"
    else:
        ai_label = "⚙️ Modus: Regelbasiert"

    if settings["fallback_enabled"]:
        fallback_label = "🔄 Fallback: Bereit"
    else:
        fallback_label = "🔄 Fallback: Aus"

    st.markdown(
        f"""
        <div class="app-topbar">
            <div class="topbar-title">AI Resume Screening</div>
            <div class="topbar-pills">
                <span class="pill">{html_escape(model_label)}</span>
                <span class="pill {api_class}">{html_escape(api_label)}</span>
                <span class="pill pill-info">{html_escape(ai_label)}</span>
                <span class="pill">{html_escape(fallback_label)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_dashboard(settings: dict) -> None:
    evaluations = get_evaluations()
    st.markdown('<h1 class="page-title">Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Kurzüberblick über den aktuellen Screening-Stand und schneller Einstieg in Demo oder Upload-Prozess.</p>',
        unsafe_allow_html=True,
    )
    render_kpis(evaluations)
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    render_dashboard_start_card(settings, evaluations)
    st.markdown('<div class="section-spacer-sm"></div>', unsafe_allow_html=True)
    render_ranking_and_detail(evaluations)


def render_upload_page(settings: dict) -> None:
    st.markdown('<h1 class="page-title">Bewerbungen hochladen</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">PDFs sammeln, Anforderungen definieren und die Analyse starten.</p>',
        unsafe_allow_html=True,
    )
    render_screening_card(settings, key_prefix="upload", expanded=True)


def render_ranking_page() -> None:
    evaluations = get_evaluations()
    st.markdown('<h1 class="page-title">Ranking</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Kandidaten nach Fit Score, Status und Skill Match vergleichen.</p>',
        unsafe_allow_html=True,
    )

    if not evaluations:
        render_empty_state("Noch kein Ranking vorhanden. Starten Sie zuerst eine Analyse.")
        return

    with st.container(border=True):
        cols = st.columns([2, 1, 1])
        with cols[0]:
            st.text_input("Suche", key="ranking_search", placeholder="Name oder Datei suchen")
        with cols[1]:
            st.selectbox(
                "Status",
                ["Alle Status", "Hohe Priorität", "Gute Priorität", "Manuell prüfen", "Niedrigere Priorität"],
                key="ranking_status_filter",
            )
        with cols[2]:
            st.slider("Mindestscore", 0, 100, key="ranking_min_score")

    filtered = filter_evaluations(evaluations)
    render_ranking_table(filtered, show_actions=True)

    selected = get_selected_candidate(filtered or evaluations)
    if selected:
        render_candidate_detail(selected)


def render_candidate_analysis_page() -> None:
    evaluations = get_evaluations()
    st.markdown('<h1 class="page-title">Kandidatenanalyse</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Detaildossier mit Score-Erklärung, Skills, offenen Punkten und Interviewfragen.</p>',
        unsafe_allow_html=True,
    )
    if not evaluations:
        render_empty_state("Noch keine Kandidatenanalyse vorhanden.")
        return

    labels = [candidate_label(evaluation) for evaluation in evaluations]
    current = get_selected_candidate(evaluations) or evaluations[0]
    current_label = candidate_label(current)
    selected_label = st.selectbox(
        "Kandidat auswählen",
        labels,
        index=labels.index(current_label) if current_label in labels else 0,
    )
    selected = evaluations[labels.index(selected_label)]
    set_selected_candidate(selected)
    render_candidate_detail(selected, expanded=True)


def render_settings_page(settings: dict) -> None:
    st.markdown('<h1 class="page-title">Einstellungen & KI-Konfiguration</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">API-Zugang, Modell und Gewichtung für das Kandidaten-Scoring konfigurieren.</p>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 2], gap="large")
    with left:
        with st.container(border=True):
            st.markdown(section_title("key", "API Settings"), unsafe_allow_html=True)
            if st.session_state.get("settings_saved_message"):
                st.success(st.session_state["settings_saved_message"])
                st.session_state["settings_saved_message"] = ""

            st.markdown(
                f'<span class="pill pill-info">Aktives Modell: {html_escape(settings["selected_model"])}</span>',
                unsafe_allow_html=True,
            )
            if not settings["api_active"]:
                st.caption("Kein API-Key aktiv: Es wird kein OpenRouter-Modell aufgerufen, die Analyse nutzt den Fallback.")

            st.checkbox("API-Key anzeigen", key="show_api_key")
            with st.form("ai_settings_form"):
                st.text_input(
                    "OpenRouter API Key",
                    key="api_key_input",
                    type="default" if st.session_state["show_api_key"] else "password",
                    placeholder="sk-or-v1-...",
                    help="Der Key wird nur in der laufenden Session verwendet oder aus der .env-Datei gelesen.",
                )
                st.selectbox(
                    "Standard-Modell",
                    MODEL_OPTIONS,
                    key="model_choice",
                    index=MODEL_OPTIONS.index(st.session_state["model_choice"])
                    if st.session_state["model_choice"] in MODEL_OPTIONS
                    else 0,
                )
                st.text_input(
                    "Anderes Modell (Modell-ID)",
                    key="custom_model_choice",
                    placeholder="z.B. openrouter/owl-alpha",
                )
                submitted = st.form_submit_button("KI-Einstellungen speichern", type="primary", use_container_width=True)

            if submitted:
                active_model = resolve_model_choice(
                    model_choice=st.session_state["model_choice"],
                    custom_model_choice=st.session_state["custom_model_choice"],
                )
                st.session_state["settings_saved_message"] = f"KI-Einstellungen gespeichert. Aktives Modell: {active_model}"
                st.rerun()

            st.caption("Andere OpenRouter-Modell-IDs können manuell eingetragen werden und überschreiben die Auswahl.")

        with st.container(border=True):
            st.markdown(section_title("tune", "Systemlogik"), unsafe_allow_html=True)
            st.toggle("KI-Analyse verwenden", key="use_ai")
            st.caption("Aktiviert das gespeicherte OpenRouter-Modell, sofern ein API-Key vorhanden ist.")
            st.toggle("Fallback-Scoring aktivieren", key="fallback_enabled")
            st.caption("Nutzt PDF-Parsing, Keyword-Matching und regelbasiertes Scoring bei fehlender oder fehlerhafter KI.")

    with right:
        with st.container(border=True):
            weights = st.session_state["score_weights"]
            st.markdown(section_title("balance", "Score Gewichtung"), unsafe_allow_html=True)
            st.caption("Speichern ist nur möglich, wenn die Summe exakt 100 Prozent ergibt.")

            pending_must = st.slider("Muss-Kriterien", 0, 100, weights["must_have"], 5, key="pending_weight_must")
            pending_nice = st.slider("Wunsch-Kriterien", 0, 100, weights["nice_to_have"], 5, key="pending_weight_nice")
            pending_skills = st.slider("Skill Match", 0, 100, weights["skills"], 5, key="pending_weight_skills")
            pending_seniority = st.slider("Erfahrung", 0, 100, weights["seniority"], 5, key="pending_weight_seniority")
            pending_ai = st.slider("KI-Bewertung", 0, 100, weights["ai_semantic"], 5, key="pending_weight_ai")
            total = pending_must + pending_nice + pending_skills + pending_seniority + pending_ai

            badge_class = "pill-success" if total == 100 else "pill-warning"
            st.markdown(
                f'<span class="pill {badge_class}">Total: {total}%</span>',
                unsafe_allow_html=True,
            )
            if st.button("Konfiguration speichern", type="primary", use_container_width=True):
                if total != 100:
                    st.error("Die Score-Gewichtung muss exakt 100 Prozent ergeben.")
                else:
                    st.session_state["score_weights"] = {
                        "must_have": pending_must,
                        "nice_to_have": pending_nice,
                        "skills": pending_skills,
                        "seniority": pending_seniority,
                        "ai_semantic": pending_ai,
                    }
                    st.success("Konfiguration gespeichert.")

    st.info(
        "Der Fit Score ist eine Entscheidungshilfe. Sensible Merkmale wie Alter, Herkunft, Geschlecht, Religion, Foto oder Familienstand werden nicht bewertet."
    )


def render_export_page() -> None:
    evaluations = get_evaluations()
    st.markdown('<h1 class="page-title">Export</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Analyseergebnisse für die manuelle HR-Prüfung exportieren.</p>',
        unsafe_allow_html=True,
    )

    if not evaluations:
        render_empty_state("Noch keine exportierbaren Ergebnisse vorhanden.")
        return

    options = [candidate_label(evaluation) for evaluation in evaluations]
    selected_labels = st.multiselect(
        "Kandidaten auswählen",
        options,
        default=options,
    )
    selected = [
        evaluation
        for evaluation in evaluations
        if candidate_label(evaluation) in selected_labels
    ]
    st.caption("Exportiert werden nur die ausgewählten Kandidaten. Es erfolgt keine dauerhafte Speicherung.")

    col_json, col_md = st.columns(2)
    with col_json:
        st.download_button(
            "JSON exportieren",
            data=export_json(selected),
            file_name="screening_ranking.json",
            mime="application/json",
            use_container_width=True,
            disabled=not selected,
        )
    with col_md:
        st.download_button(
            "Markdown exportieren",
            data=export_markdown(selected),
            file_name="screening_report.md",
            mime="text/markdown",
            use_container_width=True,
            disabled=not selected,
        )


def render_kpis(evaluations: list[CandidateEvaluation]) -> None:
    total = len(evaluations)
    avg_score = "–"
    top_candidate = "–"
    missing_must = "–"

    if evaluations:
        avg_score = f"{round(sum(e.score.total_score for e in evaluations) / total, 1)}%"
        top_candidate = evaluations[0].candidate_name
        total_must = sum(len(e.keyword_match.must_have) for e in evaluations)
        missing = sum(len(e.keyword_match.missing_must_have) for e in evaluations)
        missing_must = f"{round((missing / total_must) * 100, 1)}%" if total_must else "0%"

    items = [
        ("description", "Analysierte Bewerbungen", str(total)),
        ("analytics", "Durchschnittlicher Fit Score", avg_score),
        ("workspace_premium", "Top-Kandidat", top_candidate),
        ("warning", "Fehlende Muss-Kriterien", missing_must),
    ]
    cols = st.columns(4)
    for col, (icon, title, value) in zip(cols, items, strict=True):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon"><span class="material-symbols-outlined">{icon}</span></div>
                    <div class="kpi-title">{title}</div>
                    <div class="kpi-value">{html_escape(value)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_dashboard_start_card(
    settings: dict,
    evaluations: list[CandidateEvaluation],
) -> None:
    st.markdown(
        """
        <div class="demo-hero">
            <div class="demo-title">Prototyp sofort testen</div>
            <div class="demo-copy">
                Das Demo-Szenario nutzt eine vorbereitete Full-Stack-Stellenbeschreibung,
                passende Kriterien und mehrere Fake-Lebensläufe inklusive Randfällen.
                Ohne API-Key läuft es vollständig im regelbasierten Fallback-Modus.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    action_cols = st.columns(3)
    with action_cols[0]:
        st.markdown(
            """
            <div class="flow-step">
                <strong>1. Demo laden</strong>
                <span>Beispielrolle, Muss-/Wunsch-Kriterien und Fake-Lebensläufe werden geladen.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Demo-Szenario analysieren",
            type="primary",
            use_container_width=True,
        ):
            run_demo_scenario(settings)
            st.rerun()

    with action_cols[1]:
        st.markdown(
            """
            <div class="flow-step">
                <strong>2. Analyse ausführen</strong>
                <span>PDF-Parsing, Keyword-Matching und Scoring laufen über dieselbe Pipeline wie Uploads.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Eigene PDFs hochladen", use_container_width=True):
            navigate_to("Bewerbungen hochladen")
            st.rerun()

    with action_cols[2]:
        st.markdown(
            """
            <div class="flow-step">
                <strong>3. Ranking prüfen</strong>
                <span>Score-Erklärung, fehlende Anforderungen und Interviewfragen direkt vergleichen.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Ranking öffnen", disabled=not evaluations, use_container_width=True):
            navigate_to("Ranking")
            st.rerun()


def render_screening_card(settings: dict, key_prefix: str, expanded: bool = False) -> None:
    with st.container(border=True):
        st.markdown(section_title("upload_file", "Neues Screening starten"), unsafe_allow_html=True)
        left, right = st.columns([1.05, 1], gap="large")

        with left:
            st.markdown(
                """
                <div class="upload-shell">
                    <div class="upload-hint">
                        <div class="upload-circle"><span class="material-symbols-outlined" style="font-size:32px;">cloud_upload</span></div>
                        <strong>PDF-Lebensläufe hier auswählen</strong>
                        <span>Mehrere Dateien sind möglich</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            uploaded_files = st.file_uploader(
                "PDF-Lebensläufe",
                type=["pdf"],
                accept_multiple_files=True,
                key=f"{key_prefix}_uploaded_files",
                label_visibility="collapsed",
            )
            if uploaded_files:
                st.caption(f"{len(uploaded_files)} Datei(en) ausgewählt.")
                for file in uploaded_files:
                    st.markdown(f'<span class="chip-info">{html_escape(file.name)}</span>', unsafe_allow_html=True)

        with right:
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Beispieldaten laden", key=f"{key_prefix}_sample", use_container_width=True):
                    load_sample_data()
                    st.rerun()
            with c2:
                if st.button("Ergebnisse leeren", key=f"{key_prefix}_clear", use_container_width=True):
                    st.session_state["evaluations"] = []
                    st.session_state["selected_candidate_id"] = None
                    st.session_state["analysis_errors"] = []
                    st.session_state["last_fallback_active"] = False
                    st.session_state["last_analysis_mode"] = "Noch keine Analyse"
                    st.rerun()

            st.text_area(
                "Stellenbeschreibung",
                key="job_desc",
                height=170 if expanded else 130,
                placeholder="Stellenbeschreibung oder Anforderungskatalog einfügen...",
            )
            st.text_input(
                "Muss-Kriterien",
                key="must_have",
                placeholder="z.B. Python, SQL, REST API",
            )
            st.text_input(
                "Wunsch-Kriterien",
                key="nice_to_have",
                placeholder="z.B. Docker, React, AWS",
            )
            st.text_input(
                "Keywords und Skills",
                key="keywords",
                placeholder="z.B. Streamlit, Git, Kommunikation",
            )
            render_input_chips()

            can_use_ai = settings["use_ai"] and settings["api_active"]
            can_fallback = settings["fallback_enabled"]
            disabled = not uploaded_files or (not can_use_ai and not can_fallback)
            if not can_use_ai and can_fallback:
                st.markdown('<span class="pill pill-warning">Modus: Regelbasiert (Fallback)</span>', unsafe_allow_html=True)
            elif can_use_ai:
                st.markdown('<span class="pill pill-success">Modus: KI-gestützte Analyse</span>', unsafe_allow_html=True)
            else:
                st.warning("Aktivieren Sie Fallback-Scoring oder hinterlegen Sie einen API-Key.")


            if st.button(
                "Bewerbungen analysieren",
                type="primary",
                disabled=disabled,
                use_container_width=True,
                key=f"{key_prefix}_analyze",
            ):
                run_analysis(uploaded_files, settings)


def render_input_chips() -> None:
    groups = [
        ("Muss", split_terms(st.session_state["must_have"]), "chip-danger"),
        ("Wunsch", split_terms(st.session_state["nice_to_have"]), "chip"),
        ("Keyword", split_terms(st.session_state["keywords"]), "chip-info"),
    ]
    chips = []
    for label, terms, css_class in groups:
        for term in terms[:8]:
            chips.append(f'<span class="{css_class}">{label}: {html_escape(term)}</span>')
    if chips:
        st.markdown("".join(chips), unsafe_allow_html=True)


def run_analysis(uploaded_files: list, settings: dict) -> None:
    evaluations: list[CandidateEvaluation] = []
    errors: list[str] = []
    fallback_active = False

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, file in enumerate(uploaded_files):
        status_text.info(f"Verarbeite {file.name} ({idx + 1}/{len(uploaded_files)})...")
        try:
            evaluation, used_fallback = build_candidate_evaluation(
                pdf_bytes=file.getvalue(),
                file_name=file.name,
                settings=settings,
            )
            evaluations.append(evaluation)
            fallback_active = fallback_active or used_fallback
        except Exception as exc:
            errors.append(f"{file.name}: {exc}")

        progress_bar.progress((idx + 1) / len(uploaded_files))

    store_analysis_results(evaluations, errors, fallback_active)

    if evaluations:
        status_text.success("Analyse abgeschlossen. Das Ranking wurde aktualisiert.")
        navigate_to("Dashboard")
    else:
        status_text.error("Es wurden keine gültigen Auswertungen erzeugt.")

    for error in errors:
        st.warning(error)


def run_demo_scenario(settings: dict) -> None:
    load_sample_data(show_toast=False)
    demo_files = get_demo_resume_paths()
    if not demo_files:
        st.error("Keine Demo-Lebensläufe gefunden. Bitte prüfen Sie den Ordner sample_data/fake_resumes.")
        return

    evaluations: list[CandidateEvaluation] = []
    errors: list[str] = []
    fallback_active = False

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, path in enumerate(demo_files):
        status_text.info(f"Analysiere Demo-Lebenslauf {idx + 1}/{len(demo_files)}: {path.name}")
        try:
            evaluation, used_fallback = build_candidate_evaluation(
                pdf_bytes=path.read_bytes(),
                file_name=path.name,
                settings=settings,
            )
            evaluations.append(evaluation)
            fallback_active = fallback_active or used_fallback
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
        progress_bar.progress((idx + 1) / len(demo_files))

    store_analysis_results(evaluations, errors, fallback_active)
    if evaluations:
        status_text.success("Demo-Szenario wurde analysiert. Ranking und Kandidatendetails sind aktualisiert.")
    else:
        status_text.error("Das Demo-Szenario konnte nicht analysiert werden.")
    for error in errors:
        st.warning(error)


def build_candidate_evaluation(
    pdf_bytes: bytes,
    file_name: str,
    settings: dict,
) -> tuple[CandidateEvaluation, bool]:
    parsed_doc = extract_text_from_pdf(pdf_bytes, file_name=file_name)
    match_result = match_candidate_text(
        text=parsed_doc.text,
        must_have=st.session_state["must_have"],
        nice_to_have=st.session_state["nice_to_have"],
        keywords=st.session_state["keywords"],
    )

    wants_ai = settings["use_ai"] and settings["api_active"] and not parsed_doc.is_empty
    used_ai = False
    fallback_reason = ""

    if wants_ai:
        with st.spinner(f"KI-Analyse für {file_name} läuft..."):
            ai_analysis = analyze_resume_with_ai(
                text=parsed_doc.text,
                job_description=st.session_state["job_desc"],
                match_result=match_result,
                api_key=settings["api_key"],
                model=settings["selected_model"],
            )
        used_ai = not is_fallback_ai_analysis(ai_analysis)
        fallback_reason = ai_analysis.ai_score_reasoning if not used_ai else ""
    else:
        fallback_reason = fallback_reason_for(settings, parsed_doc.is_empty)
        ai_analysis = build_fallback_ai_analysis(match_result, reason=fallback_reason)

    if not used_ai and not settings["fallback_enabled"]:
        raise RuntimeError("Keine KI-Auswertung möglich und Fallback-Scoring ist deaktiviert.")

    candidate_name = infer_candidate_name(parsed_doc.text, file_name)
    if not used_ai:
        ai_analysis = enrich_fallback_analysis(
            ai_analysis=ai_analysis,
            match_result=match_result,
            candidate_name=candidate_name,
            fallback_reason=fallback_reason,
        )

    score_breakdown = calculate_rule_based_score(
        match_result=match_result,
        resume_text=parsed_doc.text,
        ai_fit_score=ai_analysis.ai_fit_score if used_ai else None,
        weights=settings["weights"],
    )
    candidate_name = resolve_candidate_name(ai_analysis, file_name)

    return (
        CandidateEvaluation(
            file_name=file_name,
            candidate_name=candidate_name,
            parsed_document=parsed_doc,
            keyword_match=match_result,
            score=score_breakdown,
            ai_analysis=ai_analysis,
            metadata={
                "used_ai": used_ai,
                "analysis_mode": "KI-gestützt" if used_ai else "Fallback",
                "fallback_reason": fallback_reason,
                "model": settings["selected_model"] if used_ai else "",
            },
        ),
        not used_ai,
    )


def store_analysis_results(
    evaluations: list[CandidateEvaluation],
    errors: list[str],
    fallback_active: bool,
) -> None:
    sorted_evaluations = sort_candidates(evaluations)
    st.session_state["evaluations"] = sorted_evaluations
    st.session_state["analysis_errors"] = errors
    st.session_state["last_fallback_active"] = fallback_active
    st.session_state["last_analysis_mode"] = "Regelbasiertes Fallback" if fallback_active else "KI-gestützte Analyse"

    st.session_state["selected_candidate_id"] = (
        candidate_id(sorted_evaluations[0]) if sorted_evaluations else None
    )


def get_demo_resume_paths() -> list[Path]:
    missing = [path for path in DEMO_RESUME_FILES if not path.exists()]
    if missing:
        generator_path = Path("sample_data/fake_resumes/generate_fake_resumes.py")
        if generator_path.exists():
            runpy.run_path(str(generator_path), run_name="__main__")
    return [path for path in DEMO_RESUME_FILES if path.exists()]


def enrich_fallback_analysis(
    ai_analysis: AIAnalysis,
    match_result,
    candidate_name: str,
    fallback_reason: str,
) -> AIAnalysis:
    found_must = [hit.term for hit in match_result.must_have if hit.found]
    found_nice = [hit.term for hit in match_result.nice_to_have if hit.found]
    found_keywords = [hit.term for hit in match_result.keywords if hit.found]
    missing = [*match_result.missing_must_have, *match_result.missing_nice_to_have]
    total_must = len(match_result.must_have)
    total_nice = len(match_result.nice_to_have)

    summary = (
        f"Regelbasierte Fallback-Analyse für {candidate_name}: "
        f"{len(found_must)}/{total_must or 0} Muss-Kriterien, "
        f"{len(found_nice)}/{total_nice or 0} Wunsch-Kriterien und "
        f"{len(found_keywords)} zusätzliche Keyword-Treffer erkannt. "
        f"Grund: {fallback_reason}"
    )
    strengths = [
        f"Erfülltes Muss-Kriterium: {term}" for term in found_must[:4]
    ] + [
        f"Zusätzlicher positiver Treffer: {term}" for term in [*found_nice, *found_keywords][:3]
    ]
    open_points = [
        f"Nicht im Lebenslauf gefunden oder unklar: {term}" for term in missing
    ]
    technical_questions = [
        f"Bitte erläutern Sie Ihre praktische Erfahrung mit {term}."
        for term in found_must[:3]
    ]
    clarification_questions = [
        f"Können Sie konkrete Projekterfahrung zu {term} nachreichen?"
        for term in missing[:3]
    ]
    if not technical_questions and found_keywords:
        technical_questions = [
            f"Wie haben Sie {found_keywords[0]} bisher praktisch eingesetzt?"
        ]

    return ai_analysis.model_copy(
        update={
            "candidate_name": candidate_name,
            "candidate_summary": summary,
            "strengths": strengths,
            "weaknesses_or_open_questions": open_points,
            "missing_or_unclear_requirements": missing,
            "ai_score_reasoning": fallback_reason,
            "human_review_recommendation": "Manuelle Prüfung auf Basis der regelbasierten Treffer empfohlen.",
            "interview_questions": InterviewQuestions(
                technical=technical_questions,
                clarification=clarification_questions,
            ),
            "evidence": [
                f"Keyword-Match: {term}" for term in [*found_must, *found_nice, *found_keywords][:8]
            ],
        }
    )


def render_ranking_and_detail(evaluations: list[CandidateEvaluation]) -> None:
    left, right = st.columns([2.1, 1], gap="large")
    with left:
        render_ranking_table(evaluations, show_actions=True)
    with right:
        selected = get_selected_candidate(evaluations)
        if selected:
            render_candidate_detail(selected, compact=True)
        else:
            render_empty_state("Wählen Sie einen Kandidaten aus, um Details zu sehen.")


def render_ranking_table(evaluations: list[CandidateEvaluation], show_actions: bool = True) -> None:
    with st.container(border=True):
        st.markdown(section_title("format_list_numbered", "Kandidaten-Ranking"), unsafe_allow_html=True)
        if not evaluations:
            render_empty_state("Noch keine Bewerbungen analysiert.")
            return

        st.markdown(
            """
            <div class="ranking-header">
                <div>Rang</div><div>Bewerber</div><div>Fit Score</div><div>Status</div><div>Aktion</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for rank, evaluation in enumerate(evaluations, start=1):
            row_cols = st.columns([0.45, 1.7, 1.2, 1.2, 0.95])
            selected = st.session_state["selected_candidate_id"] == candidate_id(evaluation)
            with row_cols[0]:
                st.markdown(f'<div class="rank-badge">{rank}</div>', unsafe_allow_html=True)
            with row_cols[1]:
                st.markdown(
                    f"""
                    <div class="candidate-name">{html_escape(evaluation.candidate_name)}</div>
                    <div class="candidate-meta">{html_escape(evaluation.file_name)}</div>
                    """,
                    unsafe_allow_html=True,
                )
            with row_cols[2]:
                render_score_line(evaluation.score.total_score)
            with row_cols[3]:
                label, css_class = status_for_score(evaluation.score.total_score)
                st.markdown(f'<span class="status-badge {css_class}">{label}</span>', unsafe_allow_html=True)
            with row_cols[4]:
                button_label = "Aktiv" if selected else "Details"
                if st.button(button_label, key=f"select_{candidate_id(evaluation)}", use_container_width=True):
                    set_selected_candidate(evaluation)
                    st.rerun()


def render_candidate_detail(
    evaluation: CandidateEvaluation,
    compact: bool = False,
    expanded: bool = False,
) -> None:
    ai = evaluation.ai_analysis
    match = evaluation.keyword_match
    action_state = st.session_state["review_actions"].get(candidate_id(evaluation), "Nicht markiert")

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="detail-head">
                <div>
                    <div class="candidate-name" style="font-size:20px;line-height:28px;">{html_escape(evaluation.candidate_name)}</div>
                    <div class="candidate-meta">{html_escape(evaluation.file_name)} · {html_escape(evaluation.metadata.get("analysis_mode", "Regelbasiert"))}</div>
                    <div style="margin-top:8px;"><span class="pill">{html_escape(action_state)}</span></div>
                </div>
                <div class="score-circle">{round(evaluation.score.total_score)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Kurzprofil**")
        summary = ai.candidate_summary if ai else "Keine KI-Zusammenfassung vorhanden."
        st.write(summary or "Nicht im Lebenslauf gefunden.")

        if evaluation.metadata.get("fallback_reason"):
            st.markdown(
                f'<span class="pill pill-warning">Fallback aktiv: {html_escape(evaluation.metadata["fallback_reason"])}</span>',
                unsafe_allow_html=True,
            )

        st.markdown("**Score-Erklärung**")
        st.caption(evaluation.score.explanation)
        for component in evaluation.score.components:
            st.write(f"{component.name}: {component.points} / {component.max_points} Punkte")
            st.progress(min(component.points / max(component.max_points, 1), 1.0))
            if expanded:
                st.caption(component.explanation)

        matched = [hit.term for hit in [*match.must_have, *match.nice_to_have, *match.keywords] if hit.found]
        missing = [*match.missing_must_have, *match.missing_nice_to_have]
        st.markdown("**Skill Match**")
        render_chips(matched, "chip-success", empty="Keine Treffer gefunden.")

        st.markdown("**Fehlende oder unklare Anforderungen**")
        missing_from_ai = ai.missing_or_unclear_requirements if ai else []
        render_chips(unique_strings([*missing, *missing_from_ai]), "chip-warning", empty="Keine fehlenden Anforderungen markiert.")

        if compact:
            render_interview_questions(ai, limit=3)
        else:
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Stärken**")
                render_bullets(ai.strengths if ai else [])
                st.markdown("**Offene Punkte**")
                render_bullets(ai.weaknesses_or_open_questions if ai else [])
            with cols[1]:
                render_interview_questions(ai)
                st.markdown("**Belege**")
                render_bullets(ai.evidence if ai else [])
                if ai and ai.risk_notes:
                    st.markdown("**Hinweise für manuelle Prüfung**")
                    render_bullets(ai.risk_notes)

        action_cols = st.columns(2)
        with action_cols[0]:
            if st.button("Für manuelle Prüfung vormerken", key=f"review_{candidate_id(evaluation)}", use_container_width=True):
                st.session_state["review_actions"][candidate_id(evaluation)] = "Für manuelle Prüfung vorgemerkt"
                st.rerun()
        with action_cols[1]:
            if st.button("Zur Klärung markieren", key=f"clarify_{candidate_id(evaluation)}", use_container_width=True):
                st.session_state["review_actions"][candidate_id(evaluation)] = "Klärung im Interview empfohlen"
                st.rerun()

        st.download_button(
            "Kandidatenreport als JSON",
            data=export_json(evaluation),
            file_name=f"report_{safe_filename(evaluation.candidate_name)}.json",
            mime="application/json",
            use_container_width=True,
        )


def render_interview_questions(ai: AIAnalysis | None, limit: int | None = None) -> None:
    st.markdown("**Empfohlene Interviewfragen**")
    if not ai:
        st.caption("Keine Interviewfragen vorhanden.")
        return
    questions = [
        *ai.interview_questions.technical,
        *ai.interview_questions.experience_based,
        *ai.interview_questions.clarification,
    ]
    if limit is not None:
        questions = questions[:limit]
    render_bullets(questions, empty="Keine Interviewfragen generiert.")


def render_score_line(score: float) -> None:
    width = max(0, min(100, score))
    st.markdown(
        f"""
        <div class="score-line">
            <span class="score-value">{round(score, 1)}%</span>
            <div class="score-track"><div class="score-fill" style="width:{width}%;"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chips(items: Iterable[str], css_class: str, empty: str) -> None:
    clean_items = unique_strings(items)
    if not clean_items:
        st.caption(empty)
        return
    st.markdown(
        "".join(f'<span class="{css_class}">{html_escape(item)}</span>' for item in clean_items),
        unsafe_allow_html=True,
    )


def render_bullets(items: Iterable[str], empty: str = "Nicht im Lebenslauf gefunden.") -> None:
    clean_items = unique_strings(items)
    if not clean_items:
        st.caption(empty)
        return
    for item in clean_items:
        st.write(f"- {item}")


def render_empty_state(message: str) -> None:
    st.markdown(f'<div class="empty-state">{html_escape(message)}</div>', unsafe_allow_html=True)


def render_compliance_footer() -> None:
    st.markdown(
        f"""
        <div class="compliance-footer">
            <span class="material-symbols-outlined">info</span>
            <div>{html_escape(HUMAN_REVIEW_NOTICE)} Sensible Merkmale werden nicht bewertet; fehlende Informationen werden als offen markiert.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_sample_data(show_toast: bool = True) -> None:
    try:
        job_path = Path("sample_data/sample_job_description.txt")
        keyword_path = Path("sample_data/sample_keywords.json")
        if job_path.exists():
            st.session_state["job_desc"] = job_path.read_text(encoding="utf-8")
        if keyword_path.exists():
            data = json.loads(keyword_path.read_text(encoding="utf-8"))
            st.session_state["must_have"] = ", ".join(data.get("must_have", []))
            st.session_state["nice_to_have"] = ", ".join(data.get("nice_to_have", []))
            st.session_state["keywords"] = ", ".join(data.get("keywords", []))
        if show_toast:
            st.toast("Beispieldaten geladen.")
    except Exception as exc:
        st.error(f"Beispieldaten konnten nicht geladen werden: {exc}")


def filter_evaluations(evaluations: list[CandidateEvaluation]) -> list[CandidateEvaluation]:
    search = st.session_state["ranking_search"].strip().lower()
    status_filter = st.session_state["ranking_status_filter"]
    min_score = st.session_state["ranking_min_score"]

    filtered = []
    for evaluation in evaluations:
        status, _ = status_for_score(evaluation.score.total_score)
        if status_filter != "Alle Status" and status != status_filter:
            continue
        if evaluation.score.total_score < min_score:
            continue
        if search and search not in evaluation.candidate_name.lower() and search not in evaluation.file_name.lower():
            continue
        filtered.append(evaluation)
    return filtered


def get_evaluations() -> list[CandidateEvaluation]:
    return st.session_state.get("evaluations", []) or []


def get_selected_candidate(evaluations: list[CandidateEvaluation]) -> CandidateEvaluation | None:
    if not evaluations:
        return None
    selected_id = st.session_state.get("selected_candidate_id")
    for evaluation in evaluations:
        if candidate_id(evaluation) == selected_id:
            return evaluation
    return evaluations[0]


def set_selected_candidate(evaluation: CandidateEvaluation) -> None:
    st.session_state["selected_candidate_id"] = candidate_id(evaluation)


def status_for_score(score: float) -> tuple[str, str]:
    if score >= 80:
        return "Hohe Priorität", "status-high"
    if score >= 65:
        return "Gute Priorität", "status-good"
    if score >= 50:
        return "Manuell prüfen", "status-review"
    return "Niedrigere Priorität", "status-low"


def fallback_reason_for(settings: dict, is_empty_pdf: bool) -> str:
    if is_empty_pdf:
        return "PDF enthält keinen lesbaren Text."
    if not settings["api_active"]:
        return "Kein OpenRouter API-Key hinterlegt."
    if not settings["use_ai"]:
        return "KI-Analyse deaktiviert."
    return "KI-Auswertung nicht verfügbar."


def is_fallback_ai_analysis(ai_analysis: AIAnalysis) -> bool:
    reason = f"{ai_analysis.candidate_summary} {ai_analysis.ai_score_reasoning}".lower()
    fallback_markers = [
        "kein openrouter",
        "api fehler",
        "fehler",
        "keine antwort",
        "leeren text",
        "nicht verfuegbar",
        "nicht verfügbar",
    ]
    return ai_analysis.ai_fit_score == 0 and any(marker in reason for marker in fallback_markers)


def infer_candidate_name(text: str, file_name: str) -> str:
    for line in text.splitlines()[:8]:
        cleaned = line.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered.startswith("lebenslauf -"):
            return cleaned.split("-", 1)[1].strip() or file_name_to_candidate_name(file_name)
        if lowered.startswith("resume -"):
            return cleaned.split("-", 1)[1].strip() or file_name_to_candidate_name(file_name)
    return file_name_to_candidate_name(file_name)


def resolve_candidate_name(ai_analysis: AIAnalysis, file_name: str) -> str:
    candidate_name = ai_analysis.candidate_name.strip()
    if candidate_name and candidate_name.lower() not in {"unbekannt", "unknown"}:
        return candidate_name
    return file_name_to_candidate_name(file_name)


def file_name_to_candidate_name(file_name: str) -> str:
    return Path(file_name).stem.replace("_", " ").replace("-", " ").title()


def candidate_id(evaluation: CandidateEvaluation) -> str:
    return f"{evaluation.file_name}:{evaluation.candidate_name}"


def candidate_label(evaluation: CandidateEvaluation) -> str:
    return f"{evaluation.candidate_name} ({evaluation.score.total_score}/100)"


def section_title(icon: str, label: str) -> str:
    return f'<div class="section-title"><span class="material-symbols-outlined">{icon}</span>{html_escape(label)}</div>'


def unique_strings(items: Iterable[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        value = str(item).strip()
        if not value or value.lower() in seen:
            continue
        seen.add(value.lower())
        result.append(value)
    return result


def safe_filename(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "_" for char in value)
    return "_".join(part for part in cleaned.split("_") if part) or "kandidat"


def html_escape(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


if __name__ == "__main__":
    main()
