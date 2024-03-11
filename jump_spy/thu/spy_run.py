from anchor_backtest import AnchorBackTest, DumpFormat
from security import Security

spy_def = {
    "symbol": "SPY",
    "sec_type": "ETF",
    "tick_size": 0.01,
    "tick_value": 0.01
}

spy = Security(spy_def)

anchor_config = {
    "settings":
        {
            "StDev": 50,
            "weekday": "THU",
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

anchor = AnchorBackTest(spy, anchor_config)
anchor.run_and_report()
#anchor.dump_trades(formats=[DumpFormat.STDOUT])
