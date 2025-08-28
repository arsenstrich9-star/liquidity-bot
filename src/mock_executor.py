# src/mock_executor.py

from src.broker_interface import BrokerInterface

class MockExecutor(BrokerInterface):
    def __init__(self, log_path: str = "mock_orders.log"):
        """
        Einfache Mock-Implementierung, die Orders in eine Datei schreibt
        und einen Dummy-Response zurückgibt.
        """
        self.log_path = log_path

    def submit_order(
        self,
        symbol: str,
        side: str,
        size: float,
        entry: float,
        sl: float,
        tp_levels: tuple
    ) -> dict:
        rec = f"{symbol} {side} {size} @ {entry} SL {sl} TPs {tp_levels}\n"
        with open(self.log_path, "a") as f:
            f.write(rec)
        return {"status": "mocked", "order_id": "MOCK123"}

    def get_balance(self) -> int:
        """
        Gibt einen festen Kontostand (Integer) zurück.
        """
        return 100_000
