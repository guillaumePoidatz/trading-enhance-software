import ta
 # add your own indicator and conditions to take the trade
class YourStrategy():
    """
This strategy is based on both bollinger and moving average. It is a tendance strategy
"""
    def __init__(
        self,
        df,
        usdt,
        coin,
        k_point = 0,
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
        
    def setIndicators(self):
        # -- Clear dataset --
        df = self.df

        # your indicators
        
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
            if  :
                self.longCondition = True
                self.isLong = True
            
            # -- close long market --
            # write your conditions here
            if condition1 and condition2:
                self.closeLongCondition = True
                self.isLong = False
        
        if self.use_short:
            # -- open short market --
            # write your conditions here
            if :
                self.shortCondition = True
                self.isShort = True

            # -- close short market --
            # write your conditions here
            if :
                self.closeShortCondition = True
                self.isShort = False

        return None

