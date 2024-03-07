from datetime import date, datetime
from indicators import StDev, MondayAnchor
import calendar_calcs


class LexBackTest(BackTest):
        ## indicators and tools

        self.stdev = StDev( sample_size= self.config.get('StDev', 50) )
        self.anchor = MondayAnchor(derived_len=20)
        self.holidays = calendar_calcs.load_holidays()


    def calc_analytics(self, cur_dt, bar, ref_bar):

        ## create all derived data and indicatirs here 
        self.anchor.push((cur_dt, bar))
        self.stdev.push(bar['Close'])


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
                    self.high_marker = HighestValue( bar['Open'] )
                    self.stop_level = self.calc_price_stop( self.high_marker.highest )


    def exit_CLOSE(self, cur_dt, bar, ref_bar=None):
        if self.backtest_disabled:
            return

        if self.FLAT:
            return

        pnl = bar['Close'] - self.current_trade['Entry']
        if pnl > 0:
            self.exit_trade( bar['Date'], security, bar['Close'], label='PNL' )

        elif self.current_trade['Duration'] > self.config['duration']:
            self.exit_trade( bar['Date'], security, bar['Close'], label='EXPIRY' )

        elif self.current_trade['Close'] <= self.stop_level:
            self.exit_trade( bar['Date'], security, bar['Close'], label='STOP_OUT' )


