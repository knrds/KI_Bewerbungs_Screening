from __future__ import annotations

import os
from pathlib import Path
import fitz


def create_pdf(filename: str, content: str) -> None:
    doc = fitz.open()
    page = doc.new_page()
    rect = fitz.Rect(50, 50, 550, 750)
    page.insert_textbox(rect, content, fontsize=11, fontname="helv")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc.save(filename)
    doc.close()


def generate_all() -> None:
    base_dir = Path(__file__).parent
    
    # 1. Max Mustermann (Excellent Fit)
    mustermann_content = """
    Lebenslauf - Max Mustermann
    Anschrift: Musterstraße 12, 12345 Musterstadt
    E-Mail: max.mustermann@example.com
    Telefon: +49 170 1234567

    PROFIL
    Erfahrener Senior Full-Stack Developer mit über 6 Jahren Berufserfahrung (6+ years experience) im Entwurf und der Entwicklung komplexer Webanwendungen. Expertise in Python, robusten REST-APIs, SQL-Datenbanken und modernen Frontend-Technologien. Starke Kommunikationsfähigkeiten und Erfahrung in agilen Teams.

    BERUFSERFAHRUNG
    01/2022 - Heute: Senior Full-Stack Entwickler bei Tech Solutions GmbH
    - Entwurf und Entwicklung von Microservices mit Python und FastAPI
    - Design von Datenbankarchitekturen unter Verwendung von SQL (PostgreSQL)
    - Konzeptionierung und Anbindung von sicheren REST APIs
    - Orchestrierung und Bereitstellung mittels Docker in der AWS Cloud (Amazon Web Services)
    - Enge Zusammenarbeit und strukturierte Kommunikation im Scrum-Team

    08/2019 - 12/2021: Softwareentwickler bei SoftDev AG
    - Entwicklung von Webanwendungen unter Verwendung von Python und Django
    - Erstellung von Frontends mit React und TypeScript
    - Verwaltung von Versionskontrolle mit Git

    KOMPETENZEN & SKILLS
    - Sprachen: Python, JavaScript, TypeScript, SQL
    - Frameworks & Tools: React.js, Django, FastAPI, Docker, Git
    - Cloud & Infrastruktur: AWS, REST API, PostgreSQL
    - Soft Skills: Kommunikation, Teamfähigkeit, Agile Methoden
    """
    create_pdf(str(base_dir / "max_mustermann.pdf"), mustermann_content)
    print("Created max_mustermann.pdf")

    # 2. Erika Musterfrau (Medium Fit)
    musterfrau_content = """
    Lebenslauf - Erika Musterfrau
    Anschrift: Hauptstraße 45, 54321 Stadt
    E-Mail: erika.musterfrau@example.com

    PROFIL
    Engagierte Softwareentwicklerin mit 3 Jahren Berufserfahrung (3 years experience) in der Backendentwicklung mit Python und SQL. Fokus auf Datenverarbeitung und Schnittstellen-Entwicklung (APIs). Sehr eigenverantwortliche Arbeitsweise und gute Dokumentationspraxis.

    BERUFSERFAHRUNG
    03/2023 - Heute: Backend-Entwicklerin bei DataCorp GmbH
    - Entwicklung von Datenpipelines in Python
    - Optimierung von SQL-Datenbankabfragen
    - Erstellung von API-Schnittstellen (REST API)
    - Dokumentation technischer Workflows

    01/2021 - 02/2023: Junior Developer bei CodeBase GmbH
    - Unterstützung bei der Entwicklung interner Tools mit Python
    - Pflege von Git-Repositories
    - Schnittstellentests

    KOMPETENZEN & SKILLS
    - Sprachen: Python, SQL, HTML, CSS
    - Frameworks & Tools: Django, Git
    - Sonstiges: REST API, SQL Server
    - Soft Skills: Eigenverantwortung, saubere Dokumentation
    """
    create_pdf(str(base_dir / "erika_musterfrau.pdf"), musterfrau_content)
    print("Created erika_musterfrau.pdf")

    # 3. John Doe (Poor Fit / Junior)
    doe_content = """
    Lebenslauf - John Doe
    E-Mail: john.doe@example.com

    PROFIL
    Berufseinsteiger im Bereich Webentwicklung. Erste Erfahrungen in HTML, CSS und JavaScript aus Bootcamp-Projekten. Sucht eine Einstiegsposition, um praktische Kenntnisse aufzubauen.

    BERUFSERFAHRUNG
    09/2025 - 03/2026: Web Development Bootcamp Teilnehmer
    - Aufbau von Frontend-Projekten mit HTML, CSS und JavaScript
    - Grundlagen von Git
    - Erste Erfahrungen mit kleinen Skripten in Python

    KOMPETENZEN & SKILLS
    - Sprachen: JavaScript, HTML, CSS, Grundlagen Python
    - Tools: Git, VS Code
    - Soft Skills: Lernbereitschaft, Motivation
    """
    create_pdf(str(base_dir / "john_doe.pdf"), doe_content)
    print("Created john_doe.pdf")


if __name__ == "__main__":
    generate_all()
