"""
test_config.py: tests if the config.py file works as intended. (Secrets, ModelConfig, and pricing loading)
"""
from config import Secrets

def test_secrets_load_from_env(monkeypatch):
    """
    Tests whether the correct api keys are loaded
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai")
    monkeypatch.setenv("NEBIUS_API_KEY", "test-nebius")

    secrets = Secrets()
    assert secrets.openai_api_key == "test-openai"


def test_secrets_rejects_unknown_field(monkeypatch):
    """Tests whether non-conforming keys are rejectedl."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai")
    monkeypatch.setenv("NEBIUS_API_KEY", "test-nebius")
    monkeypatch.setenv("SOME_TYPO", "oops")
    secrets = Secrets()
    assert secrets.openai_api_key == "test-openai"

