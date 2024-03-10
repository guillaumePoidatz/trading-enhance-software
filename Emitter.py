from PyQt5.QtCore import pyqtSignal, QObject

class Emitter(QObject):
    marketUpdatedSignal = pyqtSignal(list)
    backTestSignal = pyqtSignal(dict)
    backTestResultsWindowSignal = pyqtSignal(dict)
    displayBTWindowSignal = pyqtSignal(dict)
