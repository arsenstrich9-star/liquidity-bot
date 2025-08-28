# src/logger.py

import csv
import os

class TradeLogger:
    def __init__(self, filepath: str):
        """
        Erstellt den Ordner, falls nötig, und merkt sich den Pfad.
        """
        self.filepath = filepath
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        # Flag, damit Header nur einmal geschrieben wird
        self._wrote_header = False

    def log_trade(self, record: dict) -> None:
        """
        Hängt einen Trade als CSV-Zeile an. Schreibt Header nur beim ersten Mal.
        """
        write_header = not self._wrote_header and not os.path.exists(self.filepath)
        with open(self.filepath, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(record.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(record)
        self._wrote_header = True

    def export_summary(self) -> list[dict]:
        """
        Liest alle geloggten Trades ein und liefert sie als Liste von Dicts.
        """
        with open(self.filepath, newline="") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
