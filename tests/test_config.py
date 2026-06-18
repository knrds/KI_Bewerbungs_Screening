from __future__ import annotations

from config import DEFAULT_MODEL, MODEL_OPTIONS, resolve_model_choice


def test_free_openrouter_models_are_available() -> None:
    expected_models = {
        "openrouter/owl-alpha",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nex-agi/nex-n2-pro:free",
        "poolside/laguna-m.1:free",
    }

    assert expected_models.issubset(set(MODEL_OPTIONS))


def test_resolve_model_choice_uses_saved_model() -> None:
    assert resolve_model_choice("openrouter/owl-alpha", "") == "openrouter/owl-alpha"


def test_resolve_model_choice_custom_model_wins() -> None:
    assert (
        resolve_model_choice("openrouter/owl-alpha", "poolside/laguna-m.1:free")
        == "poolside/laguna-m.1:free"
    )


def test_resolve_model_choice_falls_back_to_default() -> None:
    assert resolve_model_choice("", "   ") == DEFAULT_MODEL
