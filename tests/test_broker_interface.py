import os
import tempfile
import pytest
from src.broker_interface import BrokerInterface
from src.mock_executor import MockExecutor

def test_broker_interface_is_abstract():
    # BrokerInterface darf nicht direkt instanziert werden
    with pytest.raises(TypeError):
        BrokerInterface()

def test_mock_executor_submit_order(tmp_path):
    # Log-Datei im temporären Verzeichnis anlegen
    log_file = tmp_path / "mock_orders.log"
    executor = MockExecutor(log_path=str(log_file))
    
    # Order platzieren
    res = executor.submit_order("AAPL", "buy", 2, 150.0, 149.0, [151.0, 152.0])
    
    # Prüfe Rückgabeformat
    assert isinstance(res, dict)
    assert res["status"] == "mocked"
    assert "order_id" in res
    
    # Prüfe, dass der Log-Eintrag geschrieben wurde
    content = log_file.read_text()
    assert "AAPL buy 2 @ 150.0 SL 149.0 TPs [151.0, 152.0]" in content

def test_mock_executor_get_balance():
    executor = MockExecutor()
    balance = executor.get_balance()
    assert isinstance(balance, int)
    assert balance > 0
