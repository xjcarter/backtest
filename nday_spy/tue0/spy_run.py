from nday_backtest import NdayBackTest, DumpFormat
from security import Security

spy_def = {
    "symbol": "SPY",
    "sec_type": "ETF",
    "tick_size": 0.01,
    "tick_value": 0.01
}

spy = Security(spy_def)

nday_config = {
    "settings":
        {
            "StDev": 50,
            "ma200": 200,
            "duration": 5,
            "offset": 0,
            "weekday": "TUE" 
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

nday = NdayBackTest(spy, nday_config)
nday.run_and_report()
#nday.dump_trades(formats=[DumpFormat.STDOUT])
