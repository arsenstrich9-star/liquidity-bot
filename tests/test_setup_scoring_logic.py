import pytest
from src.setup_scoring import SetupScorer

@pytest.fixture
def scorer():
    weights = {
        'OB': 0.3,
        'FVG': 0.2,
        'Sweep': 0.2,
        'GP': 0.15,
        'Momentum': 0.1,
        'Bias': 0.05
    }
    filters = {
        'volume': 1.0,
        'rsi': (3, 45, 55)
    }
    return SetupScorer(weights, filters)

def make_candles(seq):
    """Hilfsfunktion: erzeugt Kerzendicts mit Close-Werten."""
    return [{'close': v} for v in seq]

def test_detect_signals_momentum_and_bias(scorer):
    # Sequenz steigt monoton ⇒ Momentum True, Bias bleibt 'bullish'
    candles = make_candles([1, 2, 3, 4])
    signals = scorer.detect_signals(candles, bias_flag='bullish')
    assert signals['Momentum'] is True
    assert signals['Bias'] == 'bullish'

def test_apply_filters(scorer):
    # Momentum True → durchlassen
    signals = {'Momentum': True}
    assert scorer.apply_filters({'close': 0}, signals) is True

    # Momentum False → blocken
    signals['Momentum'] = False
    assert scorer.apply_filters({'close': 0}, signals) is False

def test_calculate_score_and_threshold(scorer):
    # Nur Momentum + bullish Bias aktiv
    signals = {'Momentum': True, 'Bias': 'bullish'}
    score = scorer.calculate_score(signals)
    # (0.1 + 0.05) * 100 = 15
    assert pytest.approx(score) == 15.0

    # Unter Threshold → kein Trade
    assert scorer.should_trade(score, 'bullish', 'NY') is False

    # Oberhalb Threshold → Trade
    assert scorer.should_trade(85.0, 'bullish', 'NY') is True
