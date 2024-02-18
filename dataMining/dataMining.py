import copy
import ccxt
import os
from dataMining.fromExcToRawDataStructure import fromExcToRawDataStructure
from readJsonFile import readJsonFile
from saveJsonFile import saveJsonFile

def dataMining(exchangeName,symName,tf,startDate):

    exchangeName = exchangeName
    exchange_class = getattr(ccxt, exchangeName)
    exch = exchange_class({'timeout': 10000})
    markets = exch.load_markets()
    rateLimit = exch.rateLimit

    timeframe = {'dates' : [] , 'open prices' : [] , 'highest prices' : [] , 'lowest prices' : [] , \
                  'close prices' : [] , 'volumes' : []}
    allTf = ['1w','1d','4h','1h','15m','5m']

    symbol = {}
    
    for tfUnit in allTf:
        symbol[tfUnit] = copy.deepcopy(dict(timeframe))

    exchange = {}
    new_exchange = {}
    
    folderName = 'data_Folder'
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    # init dictionnary or take precedent state
    if symName in markets:
        exchange[symName] = copy.deepcopy(dict(symbol))
        fileName = folderName+'/'+exchangeName+'_'+symName.split('/')[0]\
        +'-'+symName.split('/')[1]+'_data_History_Price_Action.json'
        if os.path.exists(fileName) :
            fileExisted = True
        else :
            fileExisted = False
        if os.path.isfile(fileName):
            exchange[symName] = readJsonFile(fileName)

    new_exchange = copy.deepcopy(exchange) 
    
    if symName in markets:   
        new_exchange[symName] = fromExcToRawDataStructure(exch,symName,exchange,rateLimit,tf,allTf,startDate,fileExisted)

    if symName in markets:
        fileName = folderName+'/'+exchangeName+'_'+symName.split('/')[0]\
        +'-'+symName.split('/')[1]+'_data_History_Price_Action.json'
            
        saveJsonFile(copy.deepcopy(new_exchange[symName]),fileName)

    return fileName
