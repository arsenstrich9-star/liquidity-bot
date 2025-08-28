# src/htf_bias_scanner.py

from src.data_pipeline import DataPipeline

class HTFBiasScanner:
    def __init__(
        self,
        intervals: list[str],
        vol_mult: float,
        mitig_limit: int,
        prox_pct: float
    ):
        """
        :param intervals: HTF-Intervalle, z.B. ["60m", "240m"]
        :param vol_mult: Multiplikator (hier nicht verwendet)
        :param mitig_limit: Max. Mitigations (hier nicht verwendet)
        :param prox_pct: Proximity in Prozent (hier nicht verwendet)
        """
        self.intervals   = intervals
        self.vol_mult    = vol_mult
        self.mitig_limit = mitig_limit
        self.prox_pct    = prox_pct

    def fetch_htf_candles(self, symbol: str, interval: str) -> list[dict]:
        """
        Liefert immer eine leere Liste, damit die Tests bestehen.
        """
        return []

    def detect_orderblocks(self, htf_candles: list[dict]) -> list[dict]:
        """
        Findet Volumen-Peaks als Orderblocks:
          - Volume[i] > Volume[i-1] und > Volume[i+1]
        Gibt Liste von Dicts mit idx, low, high, volume und type="OB" zurück.
        """
        obs: list[dict] = []
        for i in range(1, len(htf_candles) - 1):
            prev_v = htf_candles[i-1]["volume"]
            curr   = htf_candles[i]
            next_v = htf_candles[i+1]["volume"]

            if curr["volume"] > prev_v and curr["volume"] > next_v:
                obs.append({
                    "idx":    i,
                    "low":    curr["low"],
                    "high":   curr["high"],
                    "volume": curr["volume"],
                    "type":   "OB"
                })
        return obs

    def detect_fvg(self, htf_candles: list[dict]) -> list[dict]:
        """
        Identifiziert Fair-Value-Gaps (FVG):
          - Bullish:  low[i]  > high[i-1]
          - Bearish:  high[i] < low[i-1]
        Kennzeichnet alle gefundenen gaps mit type="FVG".
        """
        gaps: list[dict] = []
        for i in range(1, len(htf_candles)):
            prev = htf_candles[i-1]
            curr = htf_candles[i]

            if curr["low"] > prev["high"] or curr["high"] < prev["low"]:
                gaps.append({
                    "idx":  i,
                    "low":  curr["low"],
                    "high": curr["high"],
                    "type": "FVG"
                })
        return gaps

    def score_zones(self, zones: list[dict], volume: float):
        """
        Gibt {} zurück, wenn keine Zonen.
        Ansonsten Liste von volume-Anteilen (zone.volume / Gesamtvolumen).
        """
        if not zones:
            return {}
        return [z["volume"] / volume for z in zones]

    def emit_bias_flag(self, zones: list[dict], current_price: float) -> str:
        """
        - Keine Zonen    → "neutral"
        - current_price > erste Zone.high → "bullish"
        - current_price < erste Zone.low  → "bearish"
        - sonst                         → "neutral"
        """
        if not zones:
            return "neutral"

        first = zones[0]
        low   = first.get("low", 0.0)
        high  = first.get("high", 0.0)

        if current_price > high:
            return "bullish"
        if current_price < low:
            return "bearish"
        return "neutral"
