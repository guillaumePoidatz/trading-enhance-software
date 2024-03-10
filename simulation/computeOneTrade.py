import pandas as pd

# here is the compute of the evolution of your wallet through one trade
def computeOneTrade(strat,price,dfBackTestTf,typeOfTrade,index,tradeCharacteristics,dfTradesTf,fees):

    if typeOfTrade=='-' and (strat.usdt!=0 or strat.coin!=0) :
        strat.coin = 0
        strat.usdt = 0
        strat.isShort = False
        strat.isLong = False
    elif typeOfTrade=='long' :
        strat.enterPriceLong = price
        strat.coin = strat.usdt * fees / strat.enterPriceLong
        strat.usdt = strat.usdt - strat.usdt
    elif typeOfTrade=='close long':
        strat.closePriceLong = price
        gain = (strat.closePriceLong*fees-strat.enterPriceLong)/strat.enterPriceLong*strat.leverage+1
        strat.usdt = strat.coin * gain * strat.enterPriceLong
        strat.coin = strat.coin - strat.coin
    elif typeOfTrade=='short' :
        strat.enterPriceShort = price
        strat.coin = strat.usdt * fees / strat.enterPriceShort
        strat.usdt = strat.usdt - strat.usdt
    elif typeOfTrade=='close short':
        strat.closePriceShort = price
        gain = (strat.enterPriceShort-strat.closePriceShort*fees)/strat.enterPriceShort*strat.leverage+1
        strat.usdt = strat.coin * gain * strat.enterPriceShort
        strat.coin = strat.coin - strat.coin

    if typeOfTrade!='-':
        trade2Add = pd.DataFrame(
            [[dfBackTestTf['dates'][index],
              strat.usdt + strat.coin * price,
              typeOfTrade,
              dfBackTestTf['close prices'][index],
              str(round((1-fees)*100,4)),
              strat.usdt + strat.coin * price,
              dfBackTestTf.loc[index,'dates'].year,
              dfBackTestTf.loc[index,'dates'].month]],
            columns = tradeCharacteristics)
        dfTradesTf = dfTradesTf._append(trade2Add, ignore_index=True)
        return trade2Add,dfTradesTf
    else :
        return None

