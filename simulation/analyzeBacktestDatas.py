import importlib.util
import os
import pandas as pd
from simulation.computeBackTestTf import computeBackTestTf
import strategies.BolTrend


def analyzeBacktestDatas(timeFrameUnit,dfBackTest,generalInformations,dfTrades,years,initialUSDT,initialCoin,profitsMonth,profitsYear,stratName,fees):

    stratModule = __import__(f'strategies.{stratName}', fromlist=[stratName])
    stratClass = getattr(stratModule, stratName)
    strat = stratClass(df=dfBackTest[timeFrameUnit],
                     usdt = initialUSDT,
                     coin = 0
                     )

    dfBackTestTF = dfBackTest[timeFrameUnit]

    # buy and hold performance
    performanceBuyAndHold = initialUSDT/dfBackTestTF.loc[0,'close prices'] * dfBackTestTF.loc[len(dfBackTestTF)-1,'close prices']

    # backtest for one timeframe
    backtestDatas = computeBackTestTf(strat, dfBackTest[timeFrameUnit], initialUSDT, initialCoin,fees)
    
    # all operations necessary for general informations
    if backtestDatas['win trades']!=0 :
        profitAverage = backtestDatas['total profit']/backtestDatas['win trades']
    else :
        profitAverage = backtestDatas['total profit']
        
    if backtestDatas['loss trades'] != 0 :
        lossAverage = backtestDatas['total loss']/backtestDatas['loss trades']
    else :
        lossAverage = backtestDatas['total loss']

    if lossAverage != 0 : 
        riskReward = profitAverage / -lossAverage 
    else :
        riskReward = profitAverage
        
    startDate = dfBackTestTF['dates'][0].strftime("%Y-%m-%d")
    endDate = dfBackTestTF['dates'][len(dfBackTestTF['dates'])-1].strftime("%Y-%m-%d")
    Period = startDate + '  ' + endDate
    PnL = (backtestDatas['usdt'] + backtestDatas['coin'] * backtestDatas['last price'] - initialUSDT) / initialUSDT * 100

    if backtestDatas['number of trade'] != 0 :
        winLossRatio = backtestDatas['win trades'] / (backtestDatas['number of trade'] / 2) * 100
    else :
        winLossRatio = 0

    StratVsBnH = (backtestDatas['usdt'] + backtestDatas['coin'] * backtestDatas['last price'] - performanceBuyAndHold) / performanceBuyAndHold * 100

    if backtestDatas['number of long'] != 0 :
        winLossRatioLong = backtestDatas['win trades long'] / (backtestDatas['number of long']) * 100
    else :
        winLossRatioLong = 0

    if backtestDatas['number of short'] != 0 :
        winLossRatioShort = backtestDatas['win trades short'] / (backtestDatas['number of short']) * 100
    else :
        winLossRatioShort = 0

    gI = {
        'Period': Period,
        'PnL': str(round(PnL,2)) + ' %',
        'Strat vs Buy and Hold': str(round(StratVsBnH,2)) + ' %',
        'Win/Loss ratio': str(round(winLossRatio,2)) + ' %',
        'Risk Reward': str(round(riskReward,2)),
        'number of Trades': str(round(backtestDatas['number of trade']/2,2)),
        'Max Drawback': str(round(backtestDatas['max drawback'],2)) + ' %',
        'Win/Loss ratio short': str(round(winLossRatioShort,2)) + ' %',
        'number of Short': str(round(backtestDatas['number of short'],2)),
        'Win/Loss ratio long': str(round(winLossRatioLong,2)) + ' %',
        'number of long': str(round(backtestDatas['number of long'],2)),
        }

    index = pd.Index([0])
    generalInformations[timeFrameUnit] = pd.DataFrame(gI,index = index)

    dfTrades[timeFrameUnit] = backtestDatas['order book history timeframe']
    years[timeFrameUnit] = backtestDatas['order book per year timeframe']
    profitsMonth[timeFrameUnit] = backtestDatas['profits per month timeframe']
    profitsYear[timeFrameUnit] = backtestDatas['profits per year timeframe']
        



    
