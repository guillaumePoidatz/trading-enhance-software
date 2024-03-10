import ta
"""
Implementation of a moving average distance trading strategy
"""

class MRAT():
        def __init__(
                self,
                df,
                usdt,
                coin,
                k_point = 0,
                fast_ma_window = 10,
                slow_ma_window = 100,
                threshold_window = 20,
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
                self.fast_ma_window = fast_ma_window
                self.slow_ma_window = slow_ma_window
                self.threshold_window = threshold_window

                # set the leverage you want
                self.leverage = leverage
        def setIndicators(self):
                # -- Clear dataset --
                df = self.df
                # -- Populate indicators --
                df['fast_ma'] = ta.trend.sma_indicator(close=df['close prices'], window=self.fast_ma_window)
                df['slow_ma'] = ta.trend.sma_indicator(close=df['close prices'], window=self.slow_ma_window)
                df['mad'] = df['fast_ma'] / df['slow_ma']
                df['signal'] = ta.trend.sma_indicator(close=df['mad'], window=self.threshold_window)

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
                    condition1 = df['mad'][self.k_point] >= df['signal'][self.k_point]
                    condition2 = (self.usdt>0)
                    if condition1 & condition2:
                        self.longCondition = True
                        self.isLong = True

                    # -- close long market --
                    condition1 = df['mad'][self.k_point] < df['signal'][self.k_point]
                    condition2 = self.isLong
                    if condition1 and condition2:
                        self.closeLongCondition = True
                        self.isLong = False
                
                if self.use_short:
                    # -- open short market --
                    condition1 = df['mad'][self.k_point] > df['signal'][self.k_point]
                    condition2 = (self.usdt>0)
                    if condition1 & condition2 :
                        self.shortCondition = True
                        self.isShort = True

                    # -- close short market --
                    condition1 = df['mad'][self.k_point] >= df['signal'][self.k_point]
                    condition2 = self.isShort
                    if condition1 and condition2:
                        self.closeShortCondition = True
                        self.isShort = False

                    


                return None
