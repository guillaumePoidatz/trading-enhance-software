from PyQt5.QtCore import pyqtSignal, QObject


class Emitter(QObject):
    market_updated_signal = pyqtSignal(list)
    backtest_signal = pyqtSignal(dict)
    backtest_results_window_signal = pyqtSignal(dict)
    display_backtest_window_signal = pyqtSignal(dict)
