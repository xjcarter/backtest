from lex_backtest import LexBackTest
from security import Security

upro_def = {
    "symbol": "UPRO",
    "sec_type": "ETF",
    "tick_size": 0.01,
    "tick_value": 0.01
}

upro = Security(upro_def)

lex_config = {
    "settings":
        {
            "StDev": 50,
            "ma200": 200,
            "duration": 10
        },
    "wallet":
        {
            "cash": 10000,
            "wallet_alloc_pct": 1,
            "borrow_margin_pct": 1
        },
    "trading_limits":
        {
            "dollar_limit": 100000000,
            "position_limit": 100000,
            "leverage_target": 1
        }
}

lex = LexBackTest(upro, lex_config)
lex.run_and_report()
