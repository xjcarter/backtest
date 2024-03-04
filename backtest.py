import pandas
from datetime import date, datetime
from prettytable import PrettyTable
from indicators import StDev, MondayAnchor
import calendar_calcs

class DumpFormat(str, Enum):
    STDOUT = 'STDOUT'
    HTML = 'HTML'
    JSON = 'JSON'
    CSV = 'CSV'


class BackTest():
    def __init__(self, security, json_config, ref_index=None):

        """
        - json_config sets up params for the strategy AND 
          initial cash set up
        json_config = {
                        "settings": 
                            {
                                "StDev": 50,
                                "ma200": 200,
                                "duration": 10
                            },
                        "wallet":
                            {
                                "cash": 10000,
                                "wallet_alloc_pct": 0.5,
                                "borrow_margin_pct": 0.5
                            },
                        "trading_limits":
                            {
                                "dollar_limit": 100000000,
                                "position_limit: 100000,
                                "leverage_target": 1
                            }
        }
        """

        ## strategy settings 
        self.config = json_config
        ## Security objects
        self.security = security  
        self.ref_index = ref_index 

        self.wallet = 0 
        self.wallet_alloc_pct = 1
        self.borrow_margin_pct = 1
        self._initialize_wallet()

        self.dollar_base = None

        ## limit on capital at risk
        self.dollar_limit = None
        #W limit on position size
        self.position_limit = None
        self._initialize_limits()

        ## dict of { date, price, position, entry_label }
        self.entry = dict()  
        ## dict of { date, price, position, exit_label }
        self.exit = dict()  

        self.trades = list()
        self.trade_series = list()

        ## indicators and tools

        self.stdev = StDev(sample_size=50)
        self.anchor = MondayAnchor(derived_len=20)
        self.holidays = calendar_calcs.load_holidays()


    def _initialize_wallet(self):
        wallet_dict = self.config.get('wallet')
        if wallet_dict:
            self.wallet = wallet_dict.get('cash', 10000)
            self.wallet_alloc_pct = wallet_dict.get('wallet_alloc_pct', 1)
            self.borrow_margin_pct = wallet_dict.get('borrow_margin_pct', 1)

    def _initialize_limits(self):
        limit_dict = self.config.get('trading_limits')
        if limit_dict:
            self.dollar_limit = limit_dict.get('dollar_limit', 100000000)
            self.position_limit = limit_dict.get('position_limit', 100000)

    ## trade execution functions

    def BUY(self, price, security):
        wallet = self.config.get('wallet')
        if wallet is None: 
            return 0

        cash = wallet.get('cash', 0)
        alloc_pct = wallet('wallet_alloc_prc', 1)
        borrow_margin_pct = wallet('borrow_margin_pct', 1)
    


        pass

    def SELL(self, price, security):
        pass

    def entry_OPEN(self, cur_dt, bar, ref_bar=None):
        end_of_week = calendar_calcs.is_end_of_week(cur_dt, self.holidays)

        if self.anchor.count() > 0:
            anchor_bar, bkout = self.anchor.valueAt(0)
            if bkout < 0 and end_of_week == False:
                self.BUY( bar['Open'), self.security )

    def entry_CLOSE(self, cur_dt, bar, ref_bar=None):
        pass

    def exit_OPEN(self, cur_dt, bar, ref_bar=None):
        pass

    def exit_CLOSE(self, cur_dt, bar, ref_bar=None):
        pass


    def calc_price_stop(self):
        ## calc stop based on price distribution
        ## i.e. volatility
        pass

    def calc_drawdown_stop(self):
        ## calc stop based on percentage loss in equity
        pass


    ## position, %wallet and absolute dollar amount
    ## adjustmetn function
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


    ## post simulation functions 

    def generate_metrics(self):
        ## sharpe, etc.
        pass

    def dump_trades(self, format=DumpFormat.CSV):
        ## stdout, csv, html
        pass
    def dump_trades_series(self, format=DumpFormat.STDOUT):
        ## stdout, csv, html
        pass
    def dump_metrics(self, format=DumpFormat.STDOUT):
        ## stdout, html, and json
        pass

   
    def run(self, start_from_dt):

        start_dt = None
        if start_from_dt is not None:
            start_dt = datetime.strptime(start_from_dt,"%Y-%m-%d").date()

        holidays = calendar_calcs.load_holidays()

        # i = integer index
        # str_cur_dt= bar date string
        # cur_dt = bar datetime = datetime.strptime(dt)
        # bar = OHLC, etc data.
        for i, str_cur_dt, cur_dt, bar in self.security.next_bar():

            ref_bar = None
            if self.ref_index is not None:
                ref_bar = self.ref_index.fetch_bar(str_cur_dt)
            
            self.exit_OPEN(cur_dt, bar, ref_bar)
            self.entry_OPEN(cur_dt, bar, ref_bar)

            ## do analytics here

            self.anchor.push((cur_dt, bar))
            self.stdev.push(bar['Close'])

            # collect all analytics, but don't start trading until we
            # hit the the start_from_dt trading date
            if start_dt is not None and cur_dt < start_dt: continue

            self.exit_CLOSE(cur_dt, bar, ref_bar)
            self entry_CLOSE(cur_dt, bar, ref_bar)

            ## record trade info for thed day.

            if self.entry.get('position',0) == 0:
                self.update_position_limit()
                self.update_dollar_alloc()
                self.update_dollar_limit()

        self.generate_metrics()

        self.dump_trades()
        f or fmt in [DumpFormat.STDOUT, DumpFormat.CSV]:
            self.trade_series(fmt)
        self.dump_metrics()


