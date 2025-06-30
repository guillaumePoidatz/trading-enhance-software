from PyQt5.QtCore import QThread
import ccxt


class UpdateMarketThread(QThread):
    def __init__(self, exchange_name, emitter_instance):
        super().__init__()
        self.exchange_name = exchange_name
        self.emitter_instance = emitter_instance

    def run(self):
        exchange_instance = getattr(ccxt, self.exchange_name)
        this_exchange_instance = exchange_instance({"timeout": 10000})

        market = this_exchange_instance.load_markets()
        market = [pair for pair in market if pair.endswith("/USDT")]

        # send the signal after finishing the thread
        self.emitter_instance.market_updated_signal.emit(market)

        return None
