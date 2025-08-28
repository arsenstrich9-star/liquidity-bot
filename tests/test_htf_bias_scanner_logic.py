import pytest
from src.htf_bias_scanner import HTFBiasScanner

@pytest.fixture
def scanner():
    return HTFBiasScanner(intervals=[], vol_mult=2.0, mitig_limit=0, prox_pct=0.0)

def make_candle(vol, low, high):
    return {"volume": vol, "low": low, "high": high}

def test_detect_orderblocks(scanner):
    htf = [
        make_candle(10, 1, 2),
        make_candle(50, 2, 3),
        make_candle(5, 3, 4),
    ]
    obs = scanner.detect_orderblocks(htf)
    assert len(obs) == 1
    assert obs[0]["type"] == "OB"
    assert obs[0]["volume"] == 50

def test_detect_fvg(scanner):
    htf = [
        make_candle(1, 10, 12),
        make_candle(1, 13, 14),  # bullish FVG: low1 > high0
        make_candle(1, 15, 16),
        make_candle(1, 8,  9),   # bearish FVG: high3 < low2
        make_candle(1, 5,  6),
    ]
    fvg = scanner.detect_fvg(htf)
    idxs = [z["idx"] for z in fvg]
    assert 1 in idxs
    assert 3 in idxs
    assert all(z["type"] == "FVG" for z in fvg)

def test_score_zones_and_emit_bias_flag(scanner):
    zones = [
        {"volume": 100, "low":  90, "high":  95},
        {"volume":  50, "low": 105, "high": 110},
    ]
    scores = scanner.score_zones(zones, volume=100)
    assert pytest.approx(scores[0]) == 1.0
    assert pytest.approx(scores[1]) == 0.5

    # Bei price=100: zone0 unter Price → bullish, zone1 über Price → bearish
    flag = scanner.emit_bias_flag(zones, current_price=100)
    assert flag == "bullish"
