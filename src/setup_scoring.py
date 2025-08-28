# src/setup_scoring.py

from config import MOMENTUM_WINDOW


class SetupScorer:
    def __init__(self, weights: dict[str, float], filters: dict):
        self.weights = weights
        self.filters = filters
        self._threshold_pct = 0.8 * 100

    def detect_signals(self, candles: list[dict], bias_flag: str) -> dict:
        signals = {
            "OB": False, "FVG": False, "Sweep": False, "GP": False,
            "Momentum": False
        }
        if len(candles) > MOMENTUM_WINDOW:
            if candles[-1]["close"] > candles[-2]["close"]:
                signals["Momentum"] = True
        signals["Bias"] = bias_flag
        return signals

    def apply_filters(self, candle: dict, flags: dict) -> bool:
        """
        Jetzt: Gibt True nur zurück, wenn Momentum True.
        """
        return flags.get("Momentum", False)

    def calculate_score(self, signals: dict) -> float:
        total = 0.0
        for name, weight in self.weights.items():
            if name == "Bias":
                if signals.get("Bias") == "bullish":
                    total += weight
            else:
                if signals.get(name):
                    total += weight
        return total * 100

    def should_trade(self, score: float, bias_flag: str, session: str) -> bool:
        return bias_flag == "bullish" and score >= self._threshold_pct
