import pytest
from src.structure_engine import StructureEngine
from src.data_pipeline import DataPipeline
from config import ZIGZAG_THRESHOLD, MOMENTUM_WINDOW, SESSION_WINDOWS, TICKERS, CANDLE_INTERVALS

@pytest.fixture
def dp():
    return DataPipeline(TICKERS, CANDLE_INTERVALS, storage=None)

@pytest.fixture
def engine():
    return StructureEngine(ZIGZAG_THRESHOLD, MOMENTUM_WINDOW, SESSION_WINDOWS)

def test_detect_swings_returns_empty_list(engine, dp):
    candles = dp.fetch_historical(TICKERS[0], CANDLE_INTERVALS[0])
    swings = engine.detect_swings(candles)
    assert isinstance(swings, list)
    assert swings == []

def test_detect_bos_choch_returns_empty_dict(engine, dp):
    candles = dp.fetch_historical(TICKERS[0], CANDLE_INTERVALS[0])
    # mit leerer Swing-Liste
    result = engine.detect_bos_choch([], candles)
    assert isinstance(result, dict)
    assert result == {}
