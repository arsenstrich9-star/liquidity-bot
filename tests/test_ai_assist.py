import pytest
from src.ai_assist import AIAssist

@pytest.fixture
def ai():
    return AIAssist()

def test_defaults(ai):
    # Standard-Attribute gesetzt?
    assert ai.model == "gpt-4"
    assert ai.api_key is None

def test_summarize_market_returns_string(ai):
    res = ai.summarize_market("AAPL")
    assert isinstance(res, str)
    assert res == ""

def test_suggest_setups_returns_list(ai):
    res = ai.suggest_setups([])
    assert isinstance(res, list)
    assert res == []

def test_explain_signal_returns_string(ai):
    res = ai.explain_signal({"type": "OB"})
    assert isinstance(res, str)
    assert res == ""
