from mo_backtest import MoBackTest, DumpFormat
from security import Security

qqq_def = {
    "symbol": "QQQ",
    "sec_type": "ETF",
    "tick_size": 0.01,
    "tick_value": 0.01
}

qqq = Security(qqq_def)

mo_config = {
    "settings":
        {
            "StDev": 50,
            "Threshold": -0.02,
            "Length": 3,
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

mo = MoBackTest(qqq, mo_config)
mo.run_and_report()
#lex.dump_trades(formats=[DumpFormat.STDOUT])
