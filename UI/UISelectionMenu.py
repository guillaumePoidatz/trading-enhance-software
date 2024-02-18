from PyQt5.QtWidgets import QDialog, QWidget, QPushButton, QCheckBox, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QDateEdit
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from functools import partial

from UpdateMarketThread import UpdateMarketThread
from Emitter import Emitter

    
class UISelectionMenu(QDialog):
    def __init__(self,selectedStrat,emitterInstance):
        super().__init__()
        self.selectedStrat = selectedStrat

        # configure the main window
        self.setWindowTitle('Select your configuration')

        # combo box for exchange
        self.comboBoxExchange = QComboBox()

        labelExchange = QLabel("Select an exchange :")
        self.comboBoxExchange.addItem("binance")
        self.comboBoxExchange.addItem("bitfinex")
        #self.comboBoxExchange.addItem("bitget")
        self.comboBoxExchange.addItem("bybit")
        #self.comboBoxExchange.addItem("cryptocom")
        self.comboBoxExchange.addItem("gate")
        #self.comboBoxExchange.addItem("kraken")
        #self.comboBoxExchange.addItem("kucoin")
        #self.comboBoxExchange.addItem("mexc")
        #self.comboBoxExchange.addItem("okx")

        # check box crypto
        self.comboBoxCrypto = QComboBox()
        labelCrypto = QLabel("Select a crypto :")
        # fast research among the available pairs
        self.lineEditCryptoSearch = QLineEdit()
        self.lineEditCryptoSearch.setPlaceholderText("")
        # add a research function inside the crypto comboBox (pairs of crypto)
        self.comboBoxCrypto.setLineEdit(self.lineEditCryptoSearch)

        # to stock the markets of the exchanges that have been selected
        self.markets = dict()

        # dynamic adaptation of this comboBox Menu to the selected exchange and asyn computing
        self.exchangeName = self.comboBoxExchange.currentText()
        self.emitterInstance = emitterInstance
        self.emitterInstance.marketUpdatedSignal.connect(self.onCryptoComboBoxUpdated)
        self.comboBoxExchange.currentTextChanged.connect(self.updateCryptoComboBox)

        # start date
        self.startDate = QDateEdit()
        labelDate = QLabel("Select a date :")
        # date formatting
        self.startDate.setDisplayFormat("yyyy-MM-dd")
        # default date = current date
        self.startDate.setDate(self.startDate.date().currentDate())
        
        # timeframe
        tfUnits = ['5m','15m','1h','4h','1d','1w']
        self.allCheckBoxes = [None] * len(tfUnits)
        for tfUnitIndex in range(len(tfUnits)) :
            self.checkbox = QCheckBox(tfUnits[tfUnitIndex])
            self.allCheckBoxes[tfUnitIndex] = self.checkbox

        # Field for fees
        labelFees = QLabel("Fees percentage :")
        self.lineEditFees = QLineEdit()
        self.lineEditFees.setText("0") # default value

        # Layout for fees
        layoutFees = QVBoxLayout()
        layoutFees.addWidget(labelFees)
        layoutFees.addWidget(self.lineEditFees)
        
        # push button
        self.buttonOK = QPushButton('OK')
        self.buttonOK.clicked.connect(partial(self.checkConditions2Close, tfUnits))
        self.buttonOK.setFixedSize(100, 30)

        # layout exchange
        layoutExchange = QVBoxLayout()
        layoutExchange.setSpacing(0) 
        layoutExchange.addWidget(labelExchange)
        layoutExchange.addWidget(self.comboBoxExchange)
        
        # layout for cryptos box
        layoutCrypto = QVBoxLayout()
        layoutCrypto.addWidget(labelCrypto)
        layoutCrypto.addWidget(self.comboBoxCrypto)
        layoutCrypto.setSpacing(0)

        # layout start date
        layoutStartDate = QVBoxLayout()
        layoutStartDate.addWidget(labelDate)
        layoutStartDate.addWidget(self.startDate)
        
        # Create a horizontal layout (container) to organize crypto checkboxes
        layoutExchCryptoDate = QHBoxLayout()
        layoutExchCryptoDate.addStretch()
        layoutExchCryptoDate.addLayout(layoutExchange)
        layoutExchCryptoDate.addLayout(layoutCrypto)
        layoutExchCryptoDate.addLayout(layoutStartDate)
        layoutExchCryptoDate.addStretch()

        # layout for the timeFrames check boxes
        layoutHTimeframes = QHBoxLayout()
        layoutVTimeframes = QVBoxLayout()
        for tfUnitIndex in range(len(tfUnits)) :
            layoutHTimeframes.addWidget(self.allCheckBoxes[tfUnitIndex])
        layoutVTimeframes.addLayout(layoutHTimeframes)

        # layout for the button ok
        layoutOK = QHBoxLayout()
        layoutOK.addWidget(self.buttonOK)

        # Create a vertical layout to organize all the layouts (crypto and timeframes)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layoutExchCryptoDate)
        mainLayout.addLayout(layoutVTimeframes)
        mainLayout.addLayout(layoutOK)
        mainLayout.addLayout(layoutFees)
        
        # put sub widgets inside the main widget
        self.setLayout(mainLayout)
        self.adjustSize()

    # dynamic adaptation of crypto box to the content of exchange box
    def updateCryptoComboBox(self):

        self.comboBoxCrypto.clear()
        self.exchangeName = self.comboBoxExchange.currentText()

        # for a new exchange, we have to retrieve the market
        if self.exchangeName not in self.markets.keys():
            self.threadSelectExc = UpdateMarketThread(self.exchangeName,self.emitterInstance)
            self.threadSelectExc.start()
        # otherwise we take the recorded market
        else :
            self.onCryptoComboBoxUpdated(self.markets[self.exchangeName])

    def onCryptoComboBoxUpdated(self, market):
        if self.exchangeName not in self.markets.keys():
            # sort the market pairs
            market.sort()
            # record the available market for this exchange
            self.markets[self.exchangeName] = market
            # add the market to the UI
            self.comboBoxCrypto.addItems(market)
        else :
            self.comboBoxCrypto.addItems(self.markets[self.exchangeName])
            
    def checkConditions2Close(self,tfUnits):
        condition1 = self.comboBoxCrypto.findText(self.comboBoxCrypto.currentText()) != -1
        condition2 = self.comboBoxExchange.currentIndex()>=0
        condition3 = False
        if condition1 and condition2 :
            for tfUnit in range(len(tfUnits)) :
                if self.allCheckBoxes[tfUnit].isChecked():
                    condition3 = True
                    self.loadNewBackTest(tfUnits)
                    return None

    # load a new configurations if all the conditions are verified
    def loadNewBackTest(self,tfUnits):
        selectedTf = []
        configuration = dict()

        # -- check all the state of all the checkboxes --
        # timeframe
        for tfUnit in range(len(tfUnits)) :
            if self.allCheckBoxes[tfUnit].isChecked():
                selectedTf.append(tfUnits[tfUnit])

        # configuration
        configuration['exchange'] = self.comboBoxExchange.currentText()
        configuration['crypto'] = self.comboBoxCrypto.currentText()
        configuration['timeframes'] = selectedTf
        configuration['startDate'] = self.startDate.date()
        configuration['stratName'] = self.selectedStrat
        configuration['fees'] = float(self.lineEditFees.text())
        self.emitterInstance.backTestSignal.emit(configuration)
        self.accept()
