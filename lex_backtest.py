from datetime import date, datetime
from indicators import StDev, MondayAnchor
from backtest import BackTest, TradeType, DumpFormat
import calendar_calcs


class LexBackTest(BackTest):
    def __init__(self, security, json_config, ref_index=None):
        super().__init__(security, json_config, ref_index)

        ## needed indicators and tools

        self.settings = self.config.get('settings')

        self.stdev = StDev( sample_size= self.settings.get('StDev', 50) )
        self.anchor = MondayAnchor(derived_len=20)
        self.holidays = calendar_calcs.load_holidays()



    def calc_strategy_analytics(self, cur_dt, bar, ref_bar):

        ## create all derived data and indicatirs here 
        self.anchor.push((cur_dt, bar))
        self.stdev.push(bar['Close'])


    def exit_OPEN(self, cur_dt, bar, ref_bar=None):
        if self.backtest_disabled:
            return

        if self.FLAT:
            return

        ## if self.LONG:
        ##    self.exit_trade( bar['Date'], security, bar['Open'] )

    def entry_OPEN(self, cur_dt, bar, ref_bar=None):
        if self.backtest_disabled:
            return

        if not self.FLAT:
            return

        end_of_week = calendar_calcs.is_end_of_week(cur_dt, self.holidays)

        if self.anchor.count() > 0:
            anchor_bar, bkout = self.anchor.valueAt(0)
            if bkout < 0 and end_of_week == False:
                self.current_trade = self.enter_trade( TradeType.BUY, bar['Date'], self.security, bar['Open'], label='LEX' )
                if self.LONG:
                    initial_stop = self.initialize_stop(anchor= bar['Open'])
                    self.current_trade['StopLevel'] = self.calc_price_stop( initial_stop.highest )


    def exit_CLOSE(self, cur_dt, bar, ref_bar=None):
        if self.backtest_disabled:
            return

        if self.FLAT:
            return

        if self.LONG:

            pnl = bar['Close'] - self.current_trade['Entry']
            if pnl > 0:
                self.exit_trade( bar['Date'], self.security, bar['Close'], label='PNL' )

            elif self.current_trade['Duration'] > self.settings['duration']:
                self.exit_trade( bar['Date'], self.security, bar['Close'], label='EXPIRY' )

            elif bar['Close'] <= self.current_trade['StopLevel']:
                self.exit_trade( bar['Date'], self.security, bar['Close'], label='STOP_OUT' )


    def entry_CLOSE(self, cur_dt, bar, ref_bar=None):
        if self.backtest_disabled:
            return

        if not self.FLAT:
            return

        ## ADD entry_CLOSE SIGNAL LOGIC HERE
        ## self.current_trade = self.enter_trade( TradeType.BUY, bar['Date'], self.security, bar['Close'], label = "" )


    ## position, %wallet and absolute dollar amount
    ## adjustment functions
    ## called at the end fo every trade

    def update_position_limit(self):
        ## updates self.position_limit
        ## based on custom, strategy specific logic
        pass

    def update_wallet_alloc(self):
        ## updates self.wallet_alloc_pct
        ## based on custom, strategy specific logic
        pass

    def update_dollar_limit(self):
        ## updates self.dollar_limit
        ## based on custom, strategy specific logic
        pass
