import pytest
from src.executor import TradeExecutor

def test_place_oco_order_mock():
    exe = TradeExecutor(use_mock=True)
    res = exe.place_oco_order("AAPL", "buy", size=1, entry=100, sl=99, tp_levels=[101, 102])
    assert isinstance(res, dict)
    assert res.get("status") == "mocked"
    assert "order_id" in res
