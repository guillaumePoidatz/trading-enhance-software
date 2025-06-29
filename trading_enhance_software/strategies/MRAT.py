import ta

"""
Implementation of a moving average distance trading strategy
"""


class MRAT:
    def __init__(
        self,
        df,
        usdt,
        coin,
        k_point=0,
        fast_ma_window=10,
        slow_ma_window=100,
        threshold_window=20,
        type=["long"],
        long_condition=False,
        short_condition=False,
        close_long_condition=False,
        close_short_condition=False,
        is_long=False,
        is_short=False,
        enter_price_short=None,
        enter_price_long=None,
        close_price_short=None,
        close_price_long=None,
        leverage=1,
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
        self.fast_ma_window = fast_ma_window
        self.slow_ma_window = slow_ma_window
        self.threshold_window = threshold_window

        # set the leverage you want
        self.leverage = leverage

    def set_indicators(self):
        # -- Clear dataset --
        df = self.df
        # -- Populate indicators --
        df["fast_ma"] = ta.trend.sma_indicator(
            close=df["close prices"], window=self.fast_ma_window
        )
        df["slow_ma"] = ta.trend.sma_indicator(
            close=df["close prices"], window=self.slow_ma_window
        )
        df["mad"] = df["fast_ma"] / df["slow_ma"]
        df["signal"] = ta.trend.sma_indicator(
            close=df["mad"], window=self.threshold_window
        )

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
            condition1 = df["mad"][self.k_point] >= df["signal"][self.k_point]
            condition2 = self.usdt > 0
            if condition1 & condition2:
                self.long_condition = True
                self.is_long = True

            # -- close long market --
            condition1 = df["mad"][self.k_point] < df["signal"][self.k_point]
            condition2 = self.isLong
            if condition1 and condition2:
                self.close_long_condition = True
                self.is_long = False

        if self.use_short:
            # -- open short market --
            condition1 = df["mad"][self.k_point] > df["signal"][self.k_point]
            condition2 = self.usdt > 0
            if condition1 & condition2:
                self.short_condition = True
                self.is_short = True

            # -- close short market --
            condition1 = df["mad"][self.k_point] >= df["signal"][self.k_point]
            condition2 = self.is_short
            if condition1 and condition2:
                self.close_short_condition = True
                self.is_short = False

        return None
