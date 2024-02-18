def computeWinLossRatio(winTrades,totalProfit,lossTrades,totalLoss,profit):
    if profit > 0 :
        winTrades += 1
        totalProfit += profit
    elif profit <= 0 :
        lossTrades += 1
        totalLoss += profit

    return winTrades,totalProfit,lossTrades,totalLoss

def computeLongWinLossRatio(winTradesLong,totalProfitLong,lossTradesLong,totalLossLong,profit):
    if profit > 0 :
        winTradesLong += 1
        totalProfitLong += profit
    elif profit <= 0 :
        lossTradesLong += 1
        totalLossLong += profit

    return winTradesLong,totalProfitLong,lossTradesLong,totalLossLong

def computeShortWinLossRatio(winTradesShort,totalProfitShort,lossTradesShort,totalLossShort,profit):
    if profit > 0 :
        winTradesShort += 1
        totalProfitShort += profit
    elif profit <= 0 :
        lossTradesShort += 1
        totalLossShort += profit
        
    return winTradesShort,totalProfitShort,lossTradesShort,totalLossShort
