# src/executor.py

from src.mock_executor import MockExecutor
from src.broker_interface import BrokerInterface

class TradeExecutor:
    def __init__(self, use_mock: bool = True):
        """
        Wenn use_mock=True, wird der MockExecutor verwendet.
        Ansonsten müsste hier eine RealExecutor-Implementierung kommen.
        """
        if use_mock:
            self.client: BrokerInterface = MockExecutor()
        else:
            raise NotImplementedError("RealExecutor ist noch nicht implementiert")

    def place_oco_order(
        self,
        symbol: str,
        side: str,
        size: float,
        entry: float,
        sl: float,
        tp_levels: tuple[float, float]
    ) -> dict:
        """
        Leitet an den BrokerClient weiter.
        """
        return self.client.submit_order(
            symbol=symbol,
            side=side,
            size=size,
            entry=entry,
            sl=sl,
            tp_levels=tp_levels
        )

    def get_balance(self) -> float:
        """
        Holt das Kontoguthaben vom BrokerClient.
        """
        return self.client.get_balance()
