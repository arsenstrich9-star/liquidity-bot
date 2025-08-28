import pytest
from src.structure_engine import StructureEngine

# Beispiel-Daten: monotone Anstiege/Abfälle, zigzag_thresh=0.05 (5 %)
@pytest.fixture
def candles():
    prices = [100, 104, 110, 105, 100, 95, 102]
    return [{"timestamp": i, "open": p, "high": p, "low": p, "close": p, "volume": 1} 
            for i, p in enumerate(prices)]

@pytest.fixture
def engine():
    return StructureEngine(zigzag_thresh=0.05, momentum_window=None, sessions={})

def test_detect_swings(candles, engine):
    swings = engine.detect_swings(candles)
    # Erwarte mindestens ein Hoch (von 100→110) und ein Tief (110→100)
    types = [s["type"] for s in swings]
    assert "high" in types
    assert "low" in types

def test_detect_bos(candles, engine):
    swings = engine.detect_swings(candles)
    # Simuliere Kurs-Update oberhalb letztem Tief-Swing
    candles[-1]["close"] = 94
    result = engine.detect_bos_choch(swings, candles)
    assert "CHOCH" in result

def test_detect_no_bos_or_choch(candles, engine):
    swings = engine.detect_swings(candles)
    # Close bleibt oberhalb letztem Tief und unter letztem Hoch
    candles[-1]["close"] = 100
    result = engine.detect_bos_choch(swings, candles)
    assert result == {}
