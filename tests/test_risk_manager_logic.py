# tests/test_risk_manager_logic.py

import pandas as pd
import pytest
from src.risk_manager import compute_atr, select_tp_multiplier
from config import ATR_RANGE_THRESHOLD, REWARD_RISK

def make_candles(prices):
    """
    Hilfsfunktion: erzeugt Kerzen-Dicts, 
    bei denen high = price+1, low = price-1, close = price
    """
    return [{"high": p+1, "low": p-1, "close": p} for p in prices]

def test_compute_atr_length_and_values():
    # True Range konstant = 2 → ATR über alle Perioden > 0
    prices = [10, 12, 14, 13, 15]
    candles = make_candles(prices)
    atr = compute_atr(candles, period=3)
    # Länge stimmt
    assert len(atr) == len(prices)
    # Alle ATR-Werte positiv
    assert all(val > 0 for val in atr)

def test_select_tp_multiplier_above_threshold_defaults_to_reward_risk():
    # Konstante Preise → ATR-Verhältnis = 1 ≥ ATR_RANGE_THRESHOLD 
    # → REWARD_RISK zurückgeben
    prices = [100] * 30
    candles = make_candles(prices)
    mult = select_tp_multiplier(candles)
    assert isinstance(mult, float)
    assert pytest.approx(mult) == REWARD_RISK

def test_select_tp_multiplier_below_threshold(monkeypatch):
    # Patch compute_atr: 20-Perioden-MA ~1.0, aktueller ATR = 0.5 → ratio = 0.5 < Threshold
    def fake_compute_atr(c):
        # Serie mit 29 Werten = 1.0 und letztem Wert = 0.5
        return pd.Series([1.0] * 29 + [0.5])
    monkeypatch.setattr("src.risk_manager.compute_atr", fake_compute_atr)
    
    candles = make_candles(list(range(30)))
    mult = select_tp_multiplier(candles)
    # Nun sollten wir in den Trend‐Regime-Zweig gelangen
    assert pytest.approx(mult) == 2.5
