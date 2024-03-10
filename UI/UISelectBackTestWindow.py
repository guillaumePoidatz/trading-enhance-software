from PyQt5 import QtWidgets, QtCore
from UI.UIBackTestWindow import UIBackTestWindow

class UISelectBackTestWindow(QtWidgets.QWidget):
    def __init__(self,emitterInstance):
        super().__init__()

        self.emitterInstance = emitterInstance
        # configure the layout
        self.setWindowTitle('Select Backtest Window')
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)
        
    def action(self,tfUnit):
        BTInformations = {
            'orderBookHistory' : self.orderBookHistory[tfUnit],
            'dfBackTest' : self.dfBackTest[tfUnit],
            'generalInformations' : self.generalInformations[tfUnit],
            'fontSize' : 8,
            'dateFormat' : "%Y-%m-%d",
            'years' : self.years[tfUnit],
            'profitsMonth' : self.profitsMonth[tfUnit],
            'tfUnit':tfUnit,
            'crypto': self.crypto
            }
        self.emitterInstance.displayBTWindowSignal.emit(BTInformations)

    def updateContents(self,orderBookHistory,dfBackTest,generalInformations,profitsMonth,years, crypto, activeTf):
        self.orderBookHistory = orderBookHistory
        self.dfBackTest = dfBackTest
        self.generalInformations = generalInformations
        self.profitsMonth = profitsMonth
        self.years = years
        self.crypto = crypto
        self.activeTf = activeTf

        while self.mainLayout.count():
            child = self.mainLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # create QPushButtons
        for tfUnit in self.activeTf :
            if not orderBookHistory[tfUnit].empty:
                qBTN = QtWidgets.QPushButton()
                qBTN.setText('Back Testing timeframe ' + tfUnit)
                qBTN.clicked.connect(lambda checked, unit=tfUnit: self.action(unit))
                self.mainLayout.addWidget(qBTN)        
            
   
        
            
