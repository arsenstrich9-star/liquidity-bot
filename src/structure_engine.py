# src/structure_engine.py

class StructureEngine:
    def __init__(self, zigzag_thresh: float, momentum_window: int, sessions: dict):
        self.zigzag_thresh   = zigzag_thresh
        self.momentum_window = momentum_window
        self.sessions        = sessions

    def detect_swings(self, candles: list[dict]) -> list[dict]:
        """
        Findet lokale Hochs und Tiefs:
          - High: close[i] > close[i-1] und close[i] > close[i+1]
          - Low:  close[i] < close[i-1] und close[i] < close[i+1]
        """
        swings: list[dict] = []
        for i in range(1, len(candles) - 1):
            prev = candles[i - 1]["close"]
            curr = candles[i]["close"]
            nxt  = candles[i + 1]["close"]

            if curr > prev and curr > nxt:
                swings.append({"idx": i, "price": curr, "type": "high"})

            if curr < prev and curr < nxt:
                swings.append({"idx": i, "price": curr, "type": "low"})

        return swings

    def detect_bos_choch(self, swings: list[dict], candles: list[dict]) -> dict:
        """
        Detects Break-of-Structure (BOS) or Change-of-Character (CHOCH):
          - BOS  wenn letzter Schluss > Preis des letzten Hoch-Swings
          - CHOCH wenn letzter Schluss < Preis des letzten Tief-Swings
        Gibt nur die Keys zurück, die zutreffen, z.B. {"BOS": True}, {"CHOCH": True},
        oder {} wenn nichts zutrifft.
        """
        result: dict = {}
        latest_price = candles[-1]["close"]

        # Letzten Hoch- und Tief-Swing finden
        last_high = None
        last_low  = None
        for s in swings:
            if s["type"] == "high":
                last_high = s["price"]
            elif s["type"] == "low":
                last_low = s["price"]

        if last_high is not None and latest_price > last_high:
            result["BOS"] = True

        if last_low is not None and latest_price < last_low:
            result["CHOCH"] = True

        return result
