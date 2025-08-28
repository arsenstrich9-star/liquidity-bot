# config.py

# 1) Universe & Trading-Settings
TICKERS = [
    "AAPL", "TSLA", "NVDA", "MSFT", "AMZN",
    "META", "AMD", "GOOGL", "NFLX", "INTC"
]

# 2) Risk- und Reward-Einstellungen
RISK_PER_TRADE = 0.0025    # 0.25% des Kontostands pro Trade
REWARD_RISK    = 3.0       # klassisches Reward/Risk-Verhältnis

# 3) Daten-Intervalle & Retries
CANDLE_INTERVALS = ["1m", "5m"]
MAX_RETRIES      = 3

# 4) Struktur-Engine Parameter
ZIGZAG_THRESHOLD = 0.003   # minimaler Swing-Prozentsatz
MOMENTUM_WINDOW  = 3       # Anzahl Kerzen für Momentum-Berechnung
SESSION_WINDOWS  = {
    "NY":  ("14:30", "21:00"),
    "LDN": ("07:00", "16:00")
}

# 5) HTF-Bias-Scanner Parameter
HTF_INTERVALS               = ["60m", "240m"]
VOLUME_THRESHOLD_MULTIPLIER = 1.5
MITIGATION_LIMIT            = 2
PROXIMITY_PCT               = 0.5

# 6) Setup-Scoring Settings
WEIGHTS = {
    "OB":       0.3,
    "FVG":      0.2,
    "Sweep":    0.2,
    "GP":       0.15,
    "Momentum": 0.1,
    "Bias":     0.05
}
VOLUME_FILTER_MULT = 1.2
RSI_PERIOD, RSI_LONG, RSI_SHORT = 14, 45, 55

# 7) ATR-Regime & Risk-Management
ATR_PERIOD            = 14
ATR_RANGE_THRESHOLD   = 0.8
BREAK_EVEN_R          = 1.0

# 8) Sonstige Einstellungen
NEWS_LOOKAHEAD_MIN = 15     # Minuten-Fenster für News-Scans

# 9) Pfad für Trade-Logs
LOG_PATH = "./logs/trades.csv"
