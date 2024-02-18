# manage all types of data to feed the backtest
import ccxt
import time
import pandas as pd
from datetime import datetime,timedelta

def fromExcToRawDataStructure(exchange,symbol,rawData,rateLimit,tf,allTf,startDate,fileExisted):

    data = {}
    data[symbol] = {}

    data = rawData

    allTfOutOfTf = [tfElement for tfElement in allTf if tfElement not in tf]
    
    tfTimestamp = {
        '1w' : 7*24*3600*1000,
        '1d' : 24*3600*1000,
        '4h' : 4*3600*1000,
        '1h' : 3600*1000,
        '15m' : 15*60*1000,
        '5m' : 5*60*1000
        }
    
    # compute the limit history in one request
    ohlcv = exchange.fetch_ohlcv('BTC/USDT','1w')
    wlimit = len(ohlcv)-1
    historyLimit = {'1w':wlimit,'1d':wlimit*7,'4h' :wlimit*7*6,'1h':wlimit*7*24,
                    '15m':wlimit*7*24*4,'5m' :wlimit*7*24*12}

    # compute the start date which depending on the user command but also of the exchange history
    endDate = time.time() * 1000
    
    currentDate = datetime.now()
    targetDate = currentDate - timedelta(weeks=wlimit)
    startDate = max(startDate,int(targetDate.timestamp()) * 1000)    
    
    for tfElement in tf:
        # manage last date of the current dictionnary to reduce the time to colect datas
        if len(rawData[symbol][tfElement]['dates'])==0:
            lastDate = startDate
        else:
            lastDate = rawData[symbol][tfElement]['dates'][-1]
            
        # loop to have all the datas (history limit in one request)
        while lastDate < endDate - tfTimestamp[tfElement]:
            
            ohlcv = exchange.fetch_ohlcv(symbol,tfElement,since = lastDate, limit = historyLimit[tfElement])
            # maybe we need this line to not saturate the exchange
            # time.sleep(60/rateLimit)
            dates = []
            open_prices = []
            highest_prices = []
            lowest_prices = []
            close_prices = []
            volumes = []

        # put datas in our dictionnary, 2 possibilities : either no precedent datas or precedent datas
            if len(rawData[symbol][tfElement]['dates'])==0 or rawData[symbol][tfElement]['dates'] == -1 :
        
                for entry in ohlcv:
                
                    dates.append(entry[0])
                    open_prices.append(entry[1])
                    highest_prices.append(entry[2])
                    lowest_prices.append(entry[3])
                    close_prices.append(entry[4])
                    volumes.append(entry[5])

                data[symbol][tfElement]['dates'] = dates
                data[symbol][tfElement]['open prices'] = open_prices
                data[symbol][tfElement]['highest prices'] = highest_prices
                data[symbol][tfElement]['lowest prices'] = lowest_prices
                data[symbol][tfElement]['close prices'] = close_prices
                data[symbol][tfElement]['volumes'] = volumes

            else:
                for i in range(len(ohlcv)):
                    idx = len(ohlcv)
                    if ohlcv[i][0] == rawData[symbol][tfElement]['dates'][-1]:
                        idx = i
                        break
                    
                if idx < len(ohlcv)-1:
                    index_range = list(range(idx+1,len(ohlcv)))

                    for i in index_range:           
                        dates.append(ohlcv[i][0])
                        open_prices.append(ohlcv[i][1])
                        highest_prices.append(ohlcv[i][2])
                        lowest_prices.append(ohlcv[i][3])
                        close_prices.append(ohlcv[i][4])
                        volumes.append(ohlcv[i][5])

                    data[symbol][tfElement]['dates'] = rawData[symbol][tfElement]['dates'] + dates
                    data[symbol][tfElement]['open prices'] = rawData[symbol][tfElement]['open prices'] + open_prices
                    data[symbol][tfElement]['highest prices'] = rawData[symbol][tfElement]['highest prices'] + highest_prices
                    data[symbol][tfElement]['lowest prices'] = rawData[symbol][tfElement]['lowest prices'] + lowest_prices
                    data[symbol][tfElement]['close prices'] = rawData[symbol][tfElement]['close prices'] + close_prices
                    data[symbol][tfElement]['volumes'] = rawData[symbol][tfElement]['volumes'] + volumes
            lastDate = data[symbol][tfElement]['dates'][-1]

        # now we're stocking all the datas of the other tf to not erase our datas in the process of rewritting the dat file
        for tfElement in allTfOutOfTf :

            data[symbol][tfElement]['dates'] = rawData[symbol][tfElement]['dates']
            data[symbol][tfElement]['open prices'] = rawData[symbol][tfElement]['open prices']
            data[symbol][tfElement]['highest prices'] = rawData[symbol][tfElement]['highest prices']
            data[symbol][tfElement]['lowest prices'] = rawData[symbol][tfElement]['lowest prices']
            data[symbol][tfElement]['close prices'] = rawData[symbol][tfElement]['close prices']
            data[symbol][tfElement]['volumes'] = rawData[symbol][tfElement]['volumes']

    return data[symbol] 
