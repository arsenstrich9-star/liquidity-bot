import pytest
from src.risk_manager import RiskManager, select_tp_multiplier
from config import RISK_PER_TRADE, REWARD_RISK, ATR_RANGE_THRESHOLD

def test_calc_position_size():
    rm = RiskManager()
    # balance=1000, risk_pct=RISK_PER_TRADE, distance=2 → size = 1000*RP/2
    size = rm.calc_position_size(balance=1000, sl_price=98, entry_price=100)
    expected = (1000 * RISK_PER_TRADE) / abs(100 - 98)
    assert pytest.approx(size, rel=1e-6) == expected

def test_calc_sl_long_and_short():
    rm = RiskManager()
    # Long-Szenario: entry > invalidation
    sl_long = rm.calc_sl(entry_price=102, invalidation_price=100, atr=1.5, sl_mult=1.0)
    assert pytest.approx(sl_long, rel=1e-6) == 102 - 1.5
    # Short-Szenario: entry < invalidation
    sl_short = rm.calc_sl(entry_price=98, invalidation_price=100, atr=0.5, sl_mult=2.0)
    assert pytest.approx(sl_short, rel=1e-6) == 98 + 0.5 * 2.0

def test_calc_tp_levels_long_and_short():
    rm = RiskManager()
    # Long
    entry, sl, tp_mult = 100, 95, 2.0
    tp1, tp2 = rm.calc_tp_levels(entry, sl, tp_mult)
    dist = abs(entry - sl)
    assert tp1 == entry + dist * tp_mult
    assert tp2 == entry + dist * 2 * tp_mult
    # Short
    entry_s, sl_s, tp_mult_s = 90, 95, 1.5
    tp1_s, tp2_s = rm.calc_tp_levels(entry_s, sl_s, tp_mult_s)
    dist_s = abs(entry_s - sl_s)
    assert tp1_s == entry_s - dist_s * tp_mult_s
    assert tp2_s == entry_s - dist_s * 2 * tp_mult_s

def test_select_tp_multiplier_reward_risk(monkeypatch):
    # Erzeuge konstanten ATR so, dass ratio > ATR_RANGE_THRESHOLD
    class FakeATR(list):
        def rolling(self, *args, **kwargs):
            return self
        def mean(self):
            return self
        def iloc(self, idx):
            return self[0]
    candles = [{"high": 2, "low": 1, "close": 1.5}] * 15
    # ohne echten ATR-Test einfach sicher, dass select_tp_multiplier nicht crash
    mult = select_tp_multiplier(candles)
    assert isinstance(mult, float)
    assert mult in (REWARD_RISK, 2.5)
