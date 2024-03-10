import ta


class MovingAvgCross():

    def __init__(
        self,
        df,
        usdt,
        coin,
        k_point = 0,
        ma_window = 9,
        type=["long"],
        longCondition = False,
        shortCondition = False,
        closeLongCondition = False,
        closeShortCondition = False,
        isLong = False,
        isShort = False,
        enterPriceShort = None,
        enterPriceLong = None,
        closePriceShort = None,
        closePriceLong = None,
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
        self.longCondition = longCondition
        self.shortCondition = shortCondition
        self.closeLongCondition = closeLongCondition
        self.closeShortCondition = closeShortCondition
        self.isLong = isLong
        self.isShort = isShort
        self.usdt = usdt
        self.coin = coin
        self.enterPriceShort = enterPriceShort
        self.enterPriceLong = enterPriceLong
        self.closePriceShort = closePriceShort
        self.closePriceLong = closePriceLong
        self.ma_window = ma_window

        # set the leverage you want
        self.leverage = leverage
        
    def setIndicators(self):
        # -- Clear dataset --
        df = self.df

        # your indicators
        df['ma'] = ta.trend.sma_indicator(close=df['close prices'], window=self.ma_window)

        df['n1_close'] = df['close prices'].shift(1)
        df['n1_ma'] = df['ma'].shift(1)
        
        self.df = df    
        return self.df

    def setShortLong(self): 
        df = self.df
        # -- Initiate populate --
        self.longCondition = False
        self.shortCondition = False
        self.closeLongCondition = False
        self.closeShortCondition = False
        
        if self.use_long:
            # -- open long market --
            # write your conditions here
            condition1 = df['n1_close'][self.k_point] < df['n1_ma'][self.k_point]
            condition2 =  df['close prices'][self.k_point] > df['ma'][self.k_point]
            condition3 = (self.usdt>0)
            if condition1 and condition2 and condition3:
                self.longCondition = True
                self.isLong = True
            
            # -- close long market --
            # write your conditions here
            condition1 = df['n1_close'][self.k_point] > df['n1_ma'][self.k_point]
            condition2 = df['close prices'][self.k_point] < df['ma'][self.k_point]
            condition3 = self.isLong
            if condition1 and condition2 and condition3:
                self.closeLongCondition = True
                self.isLong = False
        
        if self.use_short:
            toto = False
            # -- open short market --
            condition4 = (self.usdt>0)
            # write your conditions here
            if toto:
                self.shortCondition = True
                self.isShort = True

            # -- close short market --
            # write your conditions here
            condition2 = self.isShort
            if toto:
                self.closeShortCondition = True
                self.isShort = False

            return None
