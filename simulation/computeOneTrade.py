import pandas as pd

def computeOneTrade(strat,usdt,coin,price,dfBackTestTf,typeOfTrade,index,tradeCharacteristics,dfTradesTf,fees):

    fees = 1 - fees / 100
    if typeOfTrade=='long' or typeOfTrade=='close short':
        coin = usdt * fees / price
        usdt = usdt - usdt
    elif typeOfTrade=='short' or typeOfTrade=='close long':
        usdt = coin * fees * price
        coin = coin - coin
       
    trade2Add = pd.DataFrame(
        [[dfBackTestTf['dates'][index],
          usdt + coin * price,
          typeOfTrade,
          dfBackTestTf['close prices'][index],
          str(round((1-fees)*100,4)),
          usdt + coin * price,
          dfBackTestTf.loc[index,'dates'].year,
          dfBackTestTf.loc[index,'dates'].month]],
        columns = tradeCharacteristics)
    
    dfTradesTf = dfTradesTf._append(trade2Add, ignore_index=True)

    strat.usdt = usdt
    strat.coin = coin

    return usdt,coin,trade2Add,dfTradesTf
