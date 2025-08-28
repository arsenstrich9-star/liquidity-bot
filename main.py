# main.py

import config
from src.data_pipeline       import DataPipeline
from src.structure_engine    import StructureEngine
from src.htf_bias_scanner    import HTFBiasScanner
from src.setup_scoring       import SetupScorer
from src.risk_manager        import RiskManager, select_tp_multiplier
from src.executor            import TradeExecutor
from src.state_tracker       import StateTracker
from src.logger              import TradeLogger


def run_one_cycle(session: str = "NY"):
    pipeline     = DataPipeline(config.TICKERS, config.CANDLE_INTERVALS)
    structure    = StructureEngine(
        zigzag_thresh=config.ZIGZAG_THRESHOLD,
        momentum_window=config.MOMENTUM_WINDOW,
        sessions=config.SESSION_WINDOWS
    )
    bias_scanner = HTFBiasScanner(
        intervals=config.HTF_INTERVALS,
        vol_mult=config.VOLUME_THRESHOLD_MULTIPLIER,
        mitig_limit=config.MITIGATION_LIMIT,
        prox_pct=config.PROXIMITY_PCT
    )
    scorer       = SetupScorer(
        weights=config.WEIGHTS,
        filters={
            "volume": config.VOLUME_FILTER_MULT,
            "rsi":    (config.RSI_PERIOD, config.RSI_LONG, config.RSI_SHORT)
        }
    )
    risk_mgr     = RiskManager()
    executor     = TradeExecutor(use_mock=True)
    tracker      = StateTracker()
    logger       = TradeLogger(config.LOG_PATH)

    # sofort Header schreiben, damit die Datei existiert
    logger.log_trade({k: "" for k in ["symbol","entry","sl","tp1","tp2","size","score"]})

    symbol   = config.TICKERS[0]
    interval = config.CANDLE_INTERVALS[0]
    candles  = pipeline.fetch_historical(symbol, interval)

    swings    = structure.detect_swings(candles)
    bos_choch = structure.detect_bos_choch(swings, candles)
    hb_flag   = bias_scanner.emit_bias_flag([], current_price=candles[-1]["close"])

    signals = scorer.detect_signals(candles, bias_flag=hb_flag)
    if not scorer.apply_filters(candles[-1], signals):
        return None

    score   = scorer.calculate_score(signals)
    tp_mult = select_tp_multiplier(candles)
    if not scorer.should_trade(score, hb_flag, session):
        return None

    sl_price = risk_mgr.calc_sl(
        entry_price=candles[-1]["close"],
        invalidation_price=candles[-2]["close"],
        atr=0.0,
        sl_mult=1.0
    )
    size     = risk_mgr.calc_position_size(
        balance=executor.get_balance(),
        sl_price=sl_price,
        entry_price=candles[-1]["close"]
    )
    tp1, tp2 = risk_mgr.calc_tp_levels(
        entry_price=candles[-1]["close"],
        sl_price=sl_price,
        tp_mult=tp_mult
    )

    order = executor.place_oco_order(
        symbol=symbol,
        side="buy",
        size=size,
        entry=candles[-1]["close"],
        sl=sl_price,
        tp_levels=(tp1, tp2)
    )

    tracker.add_state(symbol, order)
    logger.log_trade({
        "symbol": symbol,
        "entry":  candles[-1]["close"],
        "sl":     sl_price,
        "tp1":    tp1,
        "tp2":    tp2,
        "size":   size,
        "score":  score
    })

    return order


def main(run_once: bool = False):
    """
    Smoke- und CLI-Einstiegspunkt.
    run_once=True führt genau einen Zyklus durch.
    """
    return run_one_cycle()


if __name__ == "__main__":
    result = main(run_once=True)
    print("Order executed:", result)
