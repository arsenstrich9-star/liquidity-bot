# src/risk_manager.py

import pandas as pd
from config import RISK_PER_TRADE, REWARD_RISK, ATR_RANGE_THRESHOLD, ATR_PERIOD


def compute_atr(candles: list[dict], period: int = ATR_PERIOD) -> pd.Series:
    """
    Berechnet den Average True Range (ATR) über die gegebene Periode.
    Nutzt das Standard-ATR: TRUE RANGE = max(high-low, abs(high-prev_close), abs(low-prev_close))
    Liefert eine pd.Series der gleichen Länge wie 'candles'.
    """
    df = pd.DataFrame(candles)
    df["prev_close"] = df["close"].shift(1)

    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["prev_close"]).abs()
    tr3 = (df["low"] - df["prev_close"]).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period, min_periods=1).mean()
    return atr


class RiskManager:
    def __init__(self, risk_pct: float = RISK_PER_TRADE):
        """
        :param risk_pct: Anteil des Kontostands, der pro Trade riskiert wird.
        """
        self.risk_pct = risk_pct

    def calc_position_size(
        self,
        balance: float,
        sl_price: float,
        entry_price: float
    ) -> float:
        """
        Positionsgröße = (balance * risk_pct) / |entry_price - sl_price|.
        """
        distance = abs(entry_price - sl_price)
        return (balance * self.risk_pct) / distance

    def calc_sl(
        self,
        entry_price: float,
        invalidation_price: float,
        atr: float,
        sl_mult: float = 1.0
    ) -> float:
        """
        Stop-Loss:
          - Long: entry_price > invalidation_price → entry_price - atr * sl_mult
          - Short: entry_price < invalidation_price → entry_price + atr * sl_mult
        """
        if entry_price > invalidation_price:
            return entry_price - atr * sl_mult
        return entry_price + atr * sl_mult

    def calc_tp_levels(
        self,
        entry_price: float,
        sl_price: float,
        tp_mult: float
    ) -> tuple[float, float]:
        """
        Take-Profit-Levels:
          - Long:  entry + dist*tp_mult, entry + dist*tp_mult*2
          - Short: entry - dist*tp_mult, entry - dist*tp_mult*2
        """
        dist = abs(entry_price - sl_price)
        if entry_price > sl_price:
            return (
                entry_price + dist * tp_mult,
                entry_price + dist * tp_mult * 2
            )
        return (
            entry_price - dist * tp_mult,
            entry_price - dist * tp_mult * 2
        )


def select_tp_multiplier(candles: list[dict]) -> float:
    """
    Wählt den TP-Multiplier basierend auf dem ATR-Regime:
      - ATR = compute_atr(candles)
      - ATR_MA = 20-period rolling mean
      - Wenn (letzter ATR / ATR_MA) < ATR_RANGE_THRESHOLD → Trend-Regime → 2.5
      - Sonst → klassisches Reward/Risk → REWARD_RISK
    """
    atr = compute_atr(candles)
    # 20er Simple Moving Average des ATR
    atr_ma = atr.rolling(window=20, min_periods=1).mean().iloc[-1]
    last_atr = atr.iloc[-1]

    ratio = last_atr / atr_ma if atr_ma != 0 else float("inf")
    if ratio < ATR_RANGE_THRESHOLD:
        return 2.5
    return REWARD_RISK
