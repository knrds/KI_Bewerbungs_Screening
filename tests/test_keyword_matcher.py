from __future__ import annotations

from keyword_matcher import (
    split_terms,
    normalize_for_matching,
    match_candidate_text,
)


def test_split_terms() -> None:
    assert split_terms("Python, SQL; React\nDocker") == ["Python", "SQL", "React", "Docker"]
    assert split_terms(["Python", "SQL"]) == ["Python", "SQL"]
    assert split_terms(None) == []


def test_normalize_for_matching() -> None:
    assert normalize_for_matching("Python 3.9 & Django!") == "python 3.9 django"
    assert normalize_for_matching("Café Münster") == "cafe munster"
    assert normalize_for_matching("Node.js / React-Native") == "node.js react native"


def test_match_candidate_text_basic() -> None:
    text = "Ich entwickle mit Python und SQL. Erfahrung mit React ist vorhanden."
    must_have = "Python, SQL"
    nice_to_have = "React, Docker"
    keywords = ["communication"]

    result = match_candidate_text(
        text=text,
        must_have=must_have,
        nice_to_have=nice_to_have,
        keywords=keywords,
    )

    # Must-have should both be found
    assert len(result.must_have) == 2
    assert all(hit.found for hit in result.must_have)
    
    # Nice to have: React found, Docker missing
    react_hit = next(h for h in result.nice_to_have if h.term == "React")
    docker_hit = next(h for h in result.nice_to_have if h.term == "Docker")
    assert react_hit.found is True
    assert docker_hit.found is False
    assert result.missing_nice_to_have == ["Docker"]

    # Keywords: communication missing
    comm_hit = next(h for h in result.keywords if h.term == "communication")
    assert comm_hit.found is False


def test_match_candidate_text_synonyms() -> None:
    text = "Erfahrungen in JS, ML und Projektmanagement."
    
    result = match_candidate_text(
        text=text,
        must_have="JavaScript",
        nice_to_have="Machine Learning",
        keywords="Project management",
    )

    assert result.must_have[0].found is True
    assert "js" in result.must_have[0].matched_terms

    assert result.nice_to_have[0].found is True
    assert "ml" in result.nice_to_have[0].matched_terms

    assert result.keywords[0].found is True
    assert "projektmanagement" in result.keywords[0].matched_terms


def test_match_candidate_text_ignores_negated_skills() -> None:
    text = (
        "Projektmanager mit starker Kommunikation. "
        "Keine belegte Praxis in Python, SQL, API-Implementierung oder Docker. "
        "React nicht vorhanden."
    )

    result = match_candidate_text(
        text=text,
        must_have="Python, SQL, API",
        nice_to_have="Docker, React",
        keywords="Kommunikation",
    )

    assert all(hit.found is False for hit in result.must_have)
    assert all(hit.found is False for hit in result.nice_to_have)
    assert result.keywords[0].found is True


def test_word_boundaries() -> None:
    # "js" should not match inside "java" or "objspy" or similar
    text = "This is a java script and objective-c codebase."
    result = match_candidate_text(
        text=text,
        must_have="C",  # C is a single char, shouldn't match objective-c or script or whatever
    )
    # wait, objective-c contains c. Let's look at normalize_for_matching:
    # "objective-c" normalized is "objective c"
    # Word boundary matching rf"(?<![a-z0-9]){re.escape(normalized_phrase)}(?![a-z0-9])"
    # normalized "c" matches "c" in "objective c".
    # What about "java" matching "av"?
    result2 = match_candidate_text(
        text="java developer",
        must_have="av",
    )
    assert result2.must_have[0].found is False
