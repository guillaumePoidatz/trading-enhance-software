import pandas as pd
from simulation.computeYearResults import computeYearResults
from simulation.computeOneTrade import computeOneTrade
from simulation.computeWinLossRatio import computeWinLossRatio
from simulation.computeWinLossRatio import computeLongWinLossRatio
from simulation.computeWinLossRatio import computeShortWinLossRatio

def computeBackTestTf(strat,dfBackTestTf,usdt,coin,fees):
    backtestDatas = dict()
    strat.setIndicators()
    tradeCharacteristics = ['date','position','order','close price','fees','usdt size wallet','year','month']
    dfTradesTf = pd.DataFrame(columns = tradeCharacteristics) # order book history for a time frame
    yearsTf = []
    
    # useful to compute drawback
    lastAth = 0
    winTrades = 0
    lossTrades = 0
    totalLoss = 0
    totalProfit = 0
    winTradesLong = 0
    totalProfitLong = 0
    lossTradesLong = 0
    totalLossLong = 0
    winTradesShort = 0
    totalProfitShort = 0
    lossTradesShort = 0
    totalLossShort = 0
    maxDrawback = 0
    numberOfTrade = 0
    numberOfLong = 0
    numberOfShort = 0
    profitsYearTf = {}
    profitsMonthTf = {}
    profitsMonthOneYear = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0, 12 : 0}
    startYear = dfBackTestTf.loc[0,'dates'].year
    endYear = dfBackTestTf.loc[len(dfBackTestTf['dates'])-1,'dates'].year
    for i in range(startYear, endYear + 1):
        profitsMonthTf[i] = profitsMonthOneYear
        profitsYearTf[i] = 0
        
    # useful for computeYearResults
    wallet = {'precedentMonth' : 0, 'precedentMonth' : 0}
    precedent = {'Month' : '','Year' : ''}
    
    for index,price in enumerate(dfBackTestTf['close prices']) :
        strat.setShortLong()
        if strat.longCondition == True:
            # compute one trade
            usdt,coin,trade2Add,dfTradesTf = computeOneTrade(strat,usdt,coin,price,dfBackTestTf,'long',index,tradeCharacteristics,dfTradesTf,fees)
            strat.enterPriceLong = price
            
        elif strat.shortCondition == True:
            usdt,coin,trade2Add,dfTradesTf = computeOneTrade(strat,usdt,coin,price,dfBackTestTf,'short',index,tradeCharacteristics,dfTradesTf,fees)
            strat.enterPriceShort = price

        elif strat.closeLongCondition == True :
            usdt,coin,trade2Add,dfTradesTf = computeOneTrade(strat,usdt,coin,price,dfBackTestTf,'close long',index,tradeCharacteristics,dfTradesTf,fees)
            strat.closePriceLong = price
            profit = (strat.closePriceLong - strat.enterPriceLong) / strat.enterPriceLong * 100
            winTrades,totalProfit,lossTrades,totalLoss = computeWinLossRatio(winTrades,totalProfit,lossTrades,totalLoss,profit)
            winTradesLong,totalProfitLong,lossTradesLong,totalLossLong = computeLongWinLossRatio(winTradesLong,totalProfitLong,lossTradesLong,totalLossLong,profit)
            numberOfLong += 1

        elif strat.closeShortCondition == True :
            usdt,coin,trade2Add,dfTradesTf = computeOneTrade(strat,usdt,coin,price,dfBackTestTf,'close short',index,tradeCharacteristics,dfTradesTf,fees)
            strat.closePriceShort = price
            profit = (strat.closePriceShort - strat.enterPriceShort) / strat.enterPriceShort * 100
            winTrades,totalProfit,lossTrades,totalLoss = computeWinLossRatio(winTrades,totalProfit,lossTrades,totalLoss,profit)
            winTradesShort,totalProfitShort,lossTradesShort,totalLossShort = computeShortWinLossRatio(winTradesShort,totalProfitShort,lossTradesShort,totalLossShort,profit)
            numberOfShort += 1

        if strat.longCondition == True or strat.shortCondition == True or strat.closeLongCondition == True or strat.closeShortCondition == True :
            # results for each  year
            yearsTf,profitsYearTf,profitsMonthOneYear,profitsMonthTf,precedent,wallet = computeYearResults(
                numberOfTrade,
                trade2Add,
                profitsMonthOneYear,
                profitsMonthTf,
                profitsYearTf,
                yearsTf,
                precedent,
                wallet)
            numberOfTrade += 1

        strat.k_point += 1
        # compute ATH (all time high)
        lastAth = max(lastAth, usdt + coin * price)
        if (usdt + coin * price) != lastAth :
            maxDrawback = min(maxDrawback,(usdt + coin * price - lastAth)/lastAth * 100)

    backtestDatas = {
        'total profit' : totalProfit,
        'total loss' : totalLoss,
        'win trades' : winTrades,
        'loss trades' : lossTrades,
        'total profit long' : totalProfitLong,
        'total loss long' : totalLossLong,
        'win trades long' : winTradesLong,
        'loss trades long' : lossTradesLong,
        'total profit short' : totalProfitShort,
        'total loss short' : totalLossShort,
        'win trades short' : winTradesShort,
        'loss trades short' : lossTradesShort,
        'usdt' : usdt,
        'coin' : coin,
        'number of trade' : numberOfTrade,
        'number of long' : numberOfLong,
        'number of short' : numberOfShort,
        'last price' : price,
        'max drawback' : maxDrawback,
        'order book history timeframe' : dfTradesTf,
        'order book per year timeframe' : yearsTf,
        'profits per month timeframe' : profitsMonthTf,
        'profits per year timeframe' : profitsYearTf
        }
    return backtestDatas
