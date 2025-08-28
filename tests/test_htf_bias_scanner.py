import pytest
from src.htf_bias_scanner import HTFBiasScanner
from config import HTF_INTERVALS, VOLUME_THRESHOLD_MULTIPLIER, MITIGATION_LIMIT, PROXIMITY_PCT

@pytest.fixture
def scanner():
    return HTFBiasScanner(
        intervals=HTF_INTERVALS,
        vol_mult=VOLUME_THRESHOLD_MULTIPLIER,
        mitig_limit=MITIGATION_LIMIT,
        prox_pct=PROXIMITY_PCT
    )

def test_fetch_htf_candles_returns_empty(scanner):
    candles = scanner.fetch_htf_candles("AAPL", "60m")
    assert isinstance(candles, list)
    assert candles == []

def test_detect_orderblocks_returns_empty(scanner):
    obs = scanner.detect_orderblocks([])
    assert isinstance(obs, list)
    assert obs == []

def test_detect_fvg_returns_empty(scanner):
    fvg = scanner.detect_fvg([])
    assert isinstance(fvg, list)
    assert fvg == []

def test_score_zones_returns_empty_dict(scanner):
    scores = scanner.score_zones([], volume=12345)
    assert isinstance(scores, dict)
    assert scores == {}

def test_emit_bias_flag_returns_neutral(scanner):
    flag = scanner.emit_bias_flag({}, current_price=150.0)
    assert isinstance(flag, str)
    assert flag == "neutral"
