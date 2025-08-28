# src/state_tracker.py

from collections import defaultdict

class StateTracker:
    def __init__(self):
        """
        Hält pro Symbol eine Liste von States.
        """
        self.states: dict[str, list] = defaultdict(list)

    def add_state(self, symbol: str, state: object) -> None:
        """
        Fügt einen neuen State für das gegebene Symbol hinzu.
        """
        self.states[symbol].append(state)

    def get_states(self, symbol: str) -> list:
        """
        Liefert alle gespeicherten States für ein Symbol.
        """
        return self.states.get(symbol, [])
