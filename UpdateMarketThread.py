from PyQt5.QtCore import QThread, pyqtSignal
from Emitter import Emitter
import ccxt

class UpdateMarketThread(QThread):

    def __init__(self, exchangeName,emitterInstance):
        super().__init__()
        self.exchangeName = exchangeName
        self.emitterInstance = emitterInstance

    def run(self):
        exchangeInstance = getattr(ccxt, self.exchangeName)
        thisExchangeInstance = exchangeInstance({'timeout': 10000})

        market = thisExchangeInstance.load_markets()
        market = [pair for pair in market if pair.endswith("/USDT")]

        # send the signal after finishing the thread
        self.emitterInstance.marketUpdatedSignal.emit(market)
        
        return None
