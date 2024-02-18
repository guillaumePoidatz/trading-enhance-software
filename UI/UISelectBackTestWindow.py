from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from UI.UIBackTestWindow import UIBackTestWindow

class UISelectBackTestWindow(QMainWindow):
    def __init__(self,orderBookHistory,dfBackTest,generalInformations,profitsMonth,years, crypto, activeTf):
        super().__init__()
        self.orderBookHistory = orderBookHistory
        self.dfBackTest = dfBackTest
        self.generalInformations = generalInformations
        self.profitsMonth = profitsMonth
        self.years = years
        self.crypto = crypto
        self.backTestResultsWindow = None
        self.activeTf = activeTf

        # configure the main window
        window = QWidget()
        self.setWindowTitle('Select Backtest Window')

        layout = QVBoxLayout()
        # create QPushButtons
        for tfUnit in self.activeTf :
            if not orderBookHistory[tfUnit].empty:
                qBTN = QPushButton(window)
                qBTN.setText('Back Testing timeframe ' + tfUnit)
                qBTN.clicked.connect(lambda checked, unit=tfUnit: self.action(unit))
                layout.addWidget(qBTN)

        # put sub widgets inside the main widget
        self.setCentralWidget(window)
        window.setLayout(layout)
        
    def action(self,tfUnit):
        self.backTestWindow1w = UIBackTestWindow(
            orderBookHistory = self.orderBookHistory[tfUnit],
            dfBackTest = self.dfBackTest[tfUnit],
            generalInformations = self.generalInformations[tfUnit],
            fontSize = 8,
            dateFormat = "%Y-%m-%d",
            years = self.years[tfUnit],
            profitsMonth = self.profitsMonth[tfUnit]
            )
        self.backTestWindow1w.setWindowTitle('Backtest '+ tfUnit + ' ' + self.crypto)
        self.backTestWindow1w.show()
        self.backTestWindow1w.activateWindow()
            
   
        
            
