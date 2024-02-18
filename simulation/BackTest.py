from PyQt5.QtCore import QThread, pyqtSignal
import copy
import ccxt
import datetime as dt
import pandas as pd


from dataMining.dataMining import dataMining
from readJsonFile import readJsonFile
from simulation.analyzeBacktestDatas import analyzeBacktestDatas


def computeBackTest(selectedExchange,selectedCrypto,timeFrameUnits,QtPyStartDate,stratName,fees):

    timeframe = {'dates' : [] , 'open prices' : [] , 'highest prices' : [] , 'lowest prices' : [] , \
                 'close prices' : [] , 'volumes' : []}

    crypto = {'1w' : copy.deepcopy(dict(timeframe)) ,'1d' : copy.deepcopy(dict(timeframe)) ,\
              '4h' : copy.deepcopy(dict(timeframe)) ,'1h' : copy.deepcopy(dict(timeframe)), \
              '15m' : copy.deepcopy(dict(timeframe)) , '5m' : copy.deepcopy(dict(timeframe))}

    startDateDatetime = dt.datetime(QtPyStartDate.year(), QtPyStartDate.month(), QtPyStartDate.day())
    startDate = int(startDateDatetime.timestamp() * 1000)
    
    fileName = dataMining(selectedExchange,selectedCrypto,timeFrameUnits,startDate)
    crypto = readJsonFile(fileName)
    dfBackTest = dict()
    results = dict()
    
    for timeFrameUnit in timeFrameUnits :
        dfBackTest[timeFrameUnit] = pd.DataFrame(crypto[timeFrameUnit])
        # we start from the start date and we reinitialize the index
        dfBackTest[timeFrameUnit] = dfBackTest[timeFrameUnit][dfBackTest[timeFrameUnit]['dates'] >= startDate].reset_index(drop=True)
        dfBackTest[timeFrameUnit]['dates'] = pd.to_datetime(dfBackTest[timeFrameUnit]['dates'], unit='ms')

    # inital conditions
    initialUSDT = 1000
    initialCoin = 0

    # -- compute the strategy --

    # stock every trades
    dfTrades = dict() # for general informations such as the global evolution of the waller
    years = dict()
    profitsMonth = dict()
    profitsYear = dict()
    # stock the general and important informations
    generalInformations = dict()

    # backtest on each wanted dataframe, manage the global backtest
    for timeFrameUnit in timeFrameUnits:
        analyzeBacktestDatas(
            timeFrameUnit,
            dfBackTest,
            generalInformations,
            dfTrades,
            years,
            initialUSDT,
            initialCoin,
            profitsMonth,
            profitsYear,
            stratName,
            fees
            )

    results = {
        'dfTrades' : dfTrades,
        'dfBackTest' : dfBackTest,
        'generalInformations' : generalInformations,
        'profitsMonth' : profitsMonth,
        'years' : years,
        'selectedCrypto' : selectedCrypto,
        'timeFrameUnits' : timeFrameUnits
        }

    return results

class BackTest(QThread):

    def __init__(self, selectedExchange, selectedCrypto, timeFrameUnits, startDate, stratName, fees, emitterInstance):
        super().__init__()
        self.selectedExchange = selectedExchange
        self.selectedCrypto = selectedCrypto
        self.timeFrameUnits = timeFrameUnits
        self.startDate = startDate
        self.results = dict()
        self.stratName = stratName
        self.fees = fees
        self.emitterInstance = emitterInstance

    def run(self):
        results = computeBackTest(
            self.selectedExchange,
            self.selectedCrypto,
            self.timeFrameUnits,
            self.startDate,
            self.stratName,
            self.fees)
        self.emitterInstance.backTestResultsWindowSignal.emit(results)

