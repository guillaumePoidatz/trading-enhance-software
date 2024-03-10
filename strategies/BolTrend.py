import ta
      
class BolTrend():
    """
This strategy is based on both bollinger and moving average. It is a trend strategy
"""
    def __init__(
        self,
        df,
        usdt,
        coin,
        k_point = 0,
        bol_window = 100,
        bol_std = 2.25,
        long_ma_window = 500,
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
        leverage = 1,
    ):
        # dataFrame for testing
        self.df = df
        # just for backtesting (k_point of the simulation)
        self.k_point = k_point
        # do we want only long, short or both ?
        self.use_long = True if "long" in type else False
        self.use_short = True if "short" in type else False
        # number of period for bollinger band
        self.bol_window = bol_window
        # standard deviation accepted for bollinger band
        self.bol_std = bol_std
        # number of period for MA (second indicator)
        self.long_ma_window = long_ma_window
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

        # set the leverage you want
        self.leverage = leverage
        
    def setIndicators(self):
        # -- Clear dataset --
        df = self.df
        # -- Populate indicators --
        bol_band = ta.volatility.BollingerBands(close = df['close prices'], window = self.bol_window, window_dev = self.bol_std)
        # winodw number of unit for the moving average and window dev the standard deviation accepted
        df["lower_band"] = bol_band.bollinger_lband()
        df["higher_band"] = bol_band.bollinger_hband()
        df["ma_band"] = bol_band.bollinger_mavg()

        df['long_ma'] = ta.trend.sma_indicator(close=df['close prices'], window=self.long_ma_window)

        df['n1_close'] = df['close prices'].shift(1)
        df.loc[0,('n1_close')] = df.loc[0,('close prices')]

        df['n1_higher_band'] = df['higher_band'].shift(1)
        df.loc[0,('n1_higher_band')] = df.loc[0,('higher_band')]
        
        df['n1_lower_band'] = df['lower_band'].shift(1)
        df.loc[0,('n1_lower_band')] = df.loc[0,('lower_band')]
        
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
            condition1 = df['n1_close'][self.k_point] < df['n1_higher_band'][self.k_point]
            condition2 = df['close prices'][self.k_point] > df['higher_band'][self.k_point]
            condition3 = df['close prices'][self.k_point] > df['long_ma'][self.k_point]
            condition4 = (self.usdt>0)
            if condition1 & condition2 & condition3 & condition4 :
                self.longCondition = True
                self.isLong = True

            # -- close long market --
            condition1 = df['close prices'][self.k_point] < df['ma_band'][self.k_point]
            condition2 = self.isLong
            if condition1 and condition2:
                self.closeLongCondition = True
                self.isLong = False
        
        if self.use_short:
            # -- open short market --
            condition1 = df['n1_close'][self.k_point] > df['n1_lower_band'][self.k_point]
            condition2 = df['close prices'][self.k_point] < df['lower_band'][self.k_point]
            condition3 = df['close prices'][self.k_point] < df['long_ma'][self.k_point]
            condition4 = (self.usdt>0)
            if condition1 & condition2 & condition3 & condition4 :
                self.shortCondition = True
                self.isShort = True

            # -- close short market --
            condition1 = df['close prices'][self.k_point] > df['ma_band'][self.k_point]
            condition2 = self.isShort
            if condition1 and condition2:
                self.closeShortCondition = True
                self.isShort = False


        return None
