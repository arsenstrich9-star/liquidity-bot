import pytest
from src.setup_scoring import SetupScorer
from config import WEIGHTS, MOMENTUM_WINDOW, VOLUME_FILTER_MULT, RSI_PERIOD, RSI_LONG, RSI_SHORT

@pytest.fixture
def scorer():
    return SetupScorer(WEIGHTS, {
        "volume": VOLUME_FILTER_MULT,
        "rsi": (RSI_PERIOD, RSI_LONG, RSI_SHORT)
    })

def make_candles(values):
    """
    Hilfsfunktion: erstellt Kerzen-Dicts mit Close-Werten aus 'values'.
    Andere Felder werden dummy-gewertet.
    """
    return [
        {"timestamp": i, "open": v, "high": v, "low": v, "close": v, "volume": 1.0}
        for i, v in enumerate(values)
    ]

def test_detect_signals_defaults_and_momentum_false(scorer):
    # len(candles) <= MOMENTUM_WINDOW → Momentum False
    candles = make_candles(list(range(MOMENTUM_WINDOW)))
    signals = scorer.detect_signals(candles, bias_flag="neutral")
    assert signals == {
        "OB": False, "FVG": False, "Sweep": False,
        "GP": False, "Momentum": False, "Bias": "neutral"
    }

def test_detect_signals_momentum_true(scorer):
    # len(candles) > MOMENTUM_WINDOW und steigende Kurse
    seq = list(range(MOMENTUM_WINDOW + 1))
    candles = make_candles(seq)
    signals = scorer.detect_signals(candles, bias_flag="bullish")
    assert signals["Momentum"] is True
    assert signals["Bias"] == "bullish"
    # alle anderen Flags bleiben False
    for key in ("OB", "FVG", "Sweep", "GP"):
        assert signals[key] is False

def test_apply_filters_stub(scorer):
    candle = {"timestamp": 0, "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1.0}
    flags = {"OB": True, "FVG": False, "Sweep": False, "GP": False, "Momentum": True, "Bias": "bullish"}
    assert scorer.apply_filters(candle, flags) is True

def test_calculate_score_and_should_trade(scorer):
    # Signals mit OB, GP, Momentum True, bullish Bias
    signals = {"OB": True, "FVG": False, "Sweep": False, "GP": True, "Momentum": True, "Bias": "bullish"}
    score = scorer.calculate_score(signals)
    # Erwarteter Score = (0.3 + 0.15 + 0.1 + 0.05) * 100 = 60.0
    assert pytest.approx(score, rel=1e-3) == 60.0
    # 60 < 80 → kein Trade
    assert scorer.should_trade(score, signals["Bias"], session="NY") is False

    # Jetzt alle Flags True + bullish → Score = 100 → Trade
    all_signals = {k: True for k in signals}
    all_signals["Bias"] = "bullish"
    full_score = scorer.calculate_score(all_signals)
    assert pytest.approx(full_score, rel=1e-3) == 100.0
    assert scorer.should_trade(full_score, "bullish", session="NY") is True
