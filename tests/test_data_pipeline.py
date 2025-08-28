import pytest
from src.data_pipeline import DataPipeline
from config import TICKERS, CANDLE_INTERVALS

@pytest.fixture
def dp():
    # Storage=None reicht für Unit-Tests
    return DataPipeline(TICKERS, CANDLE_INTERVALS, storage=None)

def test_init_sets_attributes(dp):
    # Initialisierung speichert Ticker und Intervalle
    assert hasattr(dp, "tickers")
    assert hasattr(dp, "intervals")
    assert dp.storage is None

def test_fetch_historical_returns_list(dp):
    # Fetch liefert mindestens eine Kerze als Liste von Dicts
    data = dp.fetch_historical(TICKERS[0], CANDLE_INTERVALS[0])
    assert isinstance(data, list)
    assert len(data) > 0

def test_candle_fields(dp):
    # Jede Kerze enthält die Standard-Felder
    candles = dp.fetch_historical(TICKERS[0], CANDLE_INTERVALS[0])
    for candle in candles:
        assert isinstance(candle, dict)
        for key in ("timestamp", "open", "high", "low", "close", "volume"):
            assert key in candle
