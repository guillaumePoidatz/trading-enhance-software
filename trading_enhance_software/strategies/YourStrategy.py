import ta
# add your own indicator and conditions to take the trade
class YourStrategy():
    def __init__(
        self,
        df,
        usdt,
        coin,
        k_point = 0,
        type=["long"],
        leverage = 1,
        long_condition = False,
        short_condition = False,
        close_long_condition = False,
        close_short_condition = False,
        is_long = False,
        is_short = False,
        enter_price_short = None,
        enter_price_long = None,
        close_price_short = None,
        close_price_long = None,
        leverage = 1
    ):
        # dataFrame for testing
        self.df = df
        # just for backtesting (k_point of the simulation)
        self.k_point = k_point
        # do we want only long, short or both ?
        self.use_long = True if "long" in type else False
        self.use_short = True if "short" in type else False

        # condition for long/short
        self.long_condition = long_condition
        self.short_condition = short_condition
        self.close_long_condition = close_long_condition
        self.close_short_condition = close_short_condition
        self.is_long = is_long
        self.is_short = is_short
        self.usdt = usdt
        self.coin = coin
        self.enter_price_short = enter_price_short
        self.enter_price_long = enter_price_long
        self.close_price_short = close_price_short
        self.close_price_long = close_price_long

        # set the leverage you want
        self.leverage = leverage

def set_indicators(self):
    # -- Clear dataset --
    df = self.df

    # your indicators

    self.df = df    
    return self.df

def set_short_long(self): 
    df = self.df
    # -- Initiate populate --
    self.long_condition = False
    self.short_condition = False
    self.close_long_condition = False
    self.close_short_condition = False
    
    if self.use_long:
        # -- open long market --
        # write your conditions here
        condition4 = (self.usdt>0)
        if  :
            self.long_condition = True
            self.is_long = True
        
        # -- close long market --
        # write your conditions here
        condition2 = self.is_long
        if condition1 and condition2:
            self.close_long_condition = True
            self.isLong = False
    
    if self.use_short:
        # -- open short market --
        # write your conditions here
        condition4 = (self.usdt>0)
        if :
            self.short_condition = True
            self.is_short = True

        # -- close short market --
        # write your conditions here
        condition2 = self.is_short
        if :
            self.close_short_condition = True
            self.is_short = False

    return None
