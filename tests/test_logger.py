# tests/test_logger.py

import csv
import pytest
from src.logger import TradeLogger

def test_log_trade_creates_file_and_writes_header_and_row(tmp_path):
    # Arrangieren
    logfile = tmp_path / "trades.csv"
    logger = TradeLogger(str(logfile))
    record = {
        "symbol":      "AAPL",
        "setup_score": 78.5,
        "entry":       150.0,
        "sl":          148.0,
        "tp_levels":   [151.0, 152.0],
        "order_resp":  {"status": "mocked", "order_id": "MOCK1"}
    }

    # Agieren
    logger.log_trade(record)

    # Assert: Datei existiert
    assert logfile.exists()

    # Datei einlesen und prüfen
    with open(logfile, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Genau eine Zeile geschrieben
    assert len(rows) == 1

    # Jeden Wert gegen die record-Daten prüfen (CSV speichert alles als String)
    row = rows[0]
    for key, val in record.items():
        assert str(val) == row[key]
