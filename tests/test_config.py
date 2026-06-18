from __future__ import annotations

from config import MODEL_OPTIONS


def test_free_openrouter_models_are_available() -> None:
    expected_models = {
        "openrouter/owl-alpha",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nex-agi/nex-n2-pro:free",
        "poolside/laguna-m.1:free",
    }

    assert expected_models.issubset(set(MODEL_OPTIONS))
