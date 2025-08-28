# src/broker_interface.py

from abc import ABC, abstractmethod

class BrokerInterface(ABC):
    @abstractmethod
    def submit_order(self, symbol: str, side: str, size: float, entry: float, sl: float, tp_levels: tuple) -> dict:
        """
        Submit an OCO order.
        Must return a dict with at least 'status' and 'order_id'.
        """
        raise NotImplementedError

    @abstractmethod
    def get_balance(self) -> float:
        """
        Return the current account balance.
        """
        raise NotImplementedError
