# tests/test_integration_flow.py

import os
from pathlib     import Path
import pytest

from main        import run_one_cycle
from config      import LOG_PATH

@pytest.fixture(autouse=True)
def clean_log(tmp_path, monkeypatch):
    """
    Umleitung des Log-Pfades in ein temporäres Verzeichnis,
    damit wir keine echten Dateien beschreiben.
    """
    temp_file = tmp_path / "trades.csv"
    monkeypatch.setenv("LOG_PATH", str(temp_file))
    # Patch auch direkt das config-Attribut
    from config import LOG_PATH as orig
    monkeypatch.setitem(__import__("config").__dict__, "LOG_PATH", str(temp_file))
    yield
    # nach Test: keine Aufräumarbeiten nötig (tmp_path wird verworfen)

def test_run_one_cycle_no_trade():
    """
    Standard-Dummy-Daten lösen keinen Trade aus → None zurück.
    Hauptsache, es läuft einmal komplett durch ohne Exception.
    """
    result = run_one_cycle(session="NY")
    assert result is None

def test_run_one_cycle_creates_log_file():
    """
    Der Trade-Logger sollte auch bei None keinen Fehler werfen,
    der Log-Pfad wird aber initial angelegt.
    """
    log_path = os.getenv("LOG_PATH")
    # Noch keine Datei (sonst clean_log angelegt)
    assert not Path(log_path).exists()
    # Lauf einmal durch
    run_one_cycle(session="NY")
    # Datei existiert (mindestens Header)
    assert Path(log_path).exists()
    content = Path(log_path).read_text()
    assert "symbol,entry,sl,tp1,tp2,size,score" in content
