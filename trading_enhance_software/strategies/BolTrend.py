import ta


class BolTrend:
    """
    This strategy is based on both Bollinger Bands and a long moving average.
    It is a trend-following strategy.
    """

    def __init__(
        self,
        df,
        usdt,
        coin,
        k_point=0,
        bol_window=100,
        bol_std=2.25,
        long_ma_window=500,
        position_type=["long"],
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
        self.df = df
        self.k_point = k_point
        self.use_long = "long" in position_type
        self.use_short = "short" in position_type
        self.bol_window = bol_window
        self.bol_std = bol_std
        self.long_ma_window = long_ma_window

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
        self.leverage = leverage

    def set_indicators(self):
        df = self.df

        bol_band = ta.volatility.BollingerBands(
            close=df["close prices"], window=self.bol_window, window_dev=self.bol_std
        )

        df["lower_band"] = bol_band.bollinger_lband()
        df["higher_band"] = bol_band.bollinger_hband()
        df["ma_band"] = bol_band.bollinger_mavg()

        df["long_ma"] = ta.trend.sma_indicator(
            close=df["close prices"], window=self.long_ma_window
        )

        df["n1_close"] = df["close prices"].shift(1)
        df.loc[0, "n1_close"] = df.loc[0, "close prices"]

        df["n1_higher_band"] = df["higher_band"].shift(1)
        df.loc[0, "n1_higher_band"] = df.loc[0, "higher_band"]

        df["n1_lower_band"] = df["lower_band"].shift(1)
        df.loc[0, "n1_lower_band"] = df.loc[0, "lower_band"]

        self.df = df
        return df

    def set_short_long(self):
        df = self.df
        self.long_condition = False
        self.short_condition = False
        self.close_long_condition = False
        self.close_short_condition = False

        if self.use_long:
            # Open long condition
            cond1 = df["n1_close"][self.k_point] < df["n1_higher_band"][self.k_point]
            cond2 = df["close prices"][self.k_point] > df["higher_band"][self.k_point]
            cond3 = df["close prices"][self.k_point] > df["long_ma"][self.k_point]
            cond4 = self.usdt > 0

            if cond1 and cond2 and cond3 and cond4:
                self.long_condition = True
                self.is_long = True

            # Close long condition
            cond1 = df["close prices"][self.k_point] < df["ma_band"][self.k_point]
            cond2 = self.is_long

            if cond1 and cond2:
                self.close_long_condition = True
                self.is_long = False

        if self.use_short:
            # Open short condition
            cond1 = df["n1_close"][self.k_point] > df["n1_lower_band"][self.k_point]
            cond2 = df["close prices"][self.k_point] < df["lower_band"][self.k_point]
            cond3 = df["close prices"][self.k_point] < df["long_ma"][self.k_point]
            cond4 = self.usdt > 0

            if cond1 and cond2 and cond3 and cond4:
                self.short_condition = True
                self.is_short = True

            # Close short condition
            cond1 = df["close prices"][self.k_point] > df["ma_band"][self.k_point]
            cond2 = self.is_short  # FIXED: was `isShort` in original code

            if cond1 and cond2:
                self.close_short_condition = True
                self.is_short = False

        return None
