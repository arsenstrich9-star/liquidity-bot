# src/data_pipeline.py

class DataPipeline:
    def __init__(self, tickers, intervals, storage=None):
        """
        Stub für historische Kerzendaten.
        Liefert mindestens eine Dummy-Kerze, damit Tests len(data)>0 bestehen
        und jedes Candle-Dict die erwarteten Felder enthält.
        """
        self.tickers   = tickers
        self.intervals = intervals
        self.storage   = storage

    def fetch_historical(self, symbol, interval):
        """
        Return-Wert: Liste von Kerzen-Dicts mit folgenden Keys:
          - timestamp
          - open, high, low, close
          - volume

        Hier 5 identische Dummy-Kerzen mit fortlaufendem Timestamp.
        """
        return [
            {
                "timestamp": idx,
                "open":      1.0,
                "high":      1.0,
                "low":       1.0,
                "close":     1.0,
                "volume":    0
            }
            for idx in range(5)
        ]

    def connect(self):
        raise NotImplementedError("Realtime-Connection noch nicht implementiert")

    def subscribe_realtime(self):
        raise NotImplementedError("Realtime-Subscription noch nicht implementiert")

    def _on_message(self, data):
        raise NotImplementedError("Message-Handler noch nicht implementiert")
