from lex_backtest import LexBackTest, DumpFormat
from security import Security

es1_def = {
    "symbol": "ES1",
    "sec_type": "FUTURE",
    "tick_size": 0.25,
    "tick_value": 12.50, 
    "margin_req": 12000 
}

es1 = Security(es1_def)

lex_config = {
    "settings":
        {
            "StDev": 50,
            "ma200": 200,
            "duration": 10
        },
    "wallet":
        {
            "cash": 1000000,
            "wallet_alloc_pct": 1,
            "borrow_margin_pct": 1 
        },
    "trading_limits":
        {
            "dollar_limit": 100000000,
            "position_limit": 100000,
            "leverage_target": 3, 
        }
}

lex = LexBackTest(es1, lex_config)
lex.run_and_report()
#lex.dump_trades(formats=[DumpFormat.STDOUT])
