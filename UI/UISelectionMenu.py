import os
from PyQt5 import QtWidgets, QtCore
from functools import partial

from UpdateMarketThread import UpdateMarketThread
from Emitter import Emitter
from UI.CodeEditor import CodeEditor
from UI.highlighter.pyHighlight import PythonHighlighter

class UISelectionMenu(QtWidgets.QWidget):
    def __init__(self,selectedStrat,emitterInstance,strategies_path):
        super().__init__()
        self.selectedStrat = selectedStrat

        # configure the main window
        self.setWindowTitle('Select your configuration')

        # combo box for exchange
        self.comboBoxExchange = QtWidgets.QComboBox()

        labelExchange = QtWidgets.QLabel("Select an exchange :")
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

        # to stock the markets of the exchanges that have been selected
        self.markets = dict()

        # dynamic adaptation of this comboBox Menu to the selected exchange and asyn computing
        self.exchangeName = self.comboBoxExchange.currentText()
        self.emitterInstance = emitterInstance
        self.emitterInstance.marketUpdatedSignal.connect(self.onCryptoComboBoxUpdated)
        self.comboBoxExchange.currentTextChanged.connect(self.updateCryptoComboBox)

        # start date
        self.startDate = QtWidgets.QDateEdit()
        labelDate = QtWidgets.QLabel("Select a date :")
        # date formatting
        self.startDate.setDisplayFormat("yyyy-MM-dd")
        # default date = current date
        self.startDate.setDate(self.startDate.date().currentDate())
        
        # timeframe
        tfUnits = ['5m','15m','1h','4h','1d','1w']
        self.allCheckBoxes = [None] * len(tfUnits)
        for tfUnitIndex in range(len(tfUnits)) :
            self.checkbox = QtWidgets.QCheckBox(tfUnits[tfUnitIndex])
            self.allCheckBoxes[tfUnitIndex] = self.checkbox

        # Field for tab containing cryptos and wallet size dedicated
        self.tableCryptoSize = QtWidgets.QTableWidget(1, 2)
        self.tableCryptoSize.setColumnWidth(0, 120)
        self.tableCryptoSize.verticalHeader().hide()
        self.tableCryptoSize.setHorizontalHeaderLabels(["Crypto","Size (%)"])
        self.tableCryptoSize.setFixedSize(220,self.tableCryptoSize.height())
        protoItem = QtWidgets.QTableWidgetItem()
        protoItem.setSizeHint(QtCore.QSize(150, 50))
        protoItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableCryptoSize.setItemPrototype(protoItem)
        
        # Field for cryptos
        self.comboBoxCryptos=[]
        comboBoxCrypto = QtWidgets.QComboBox()
        comboBoxCrypto.setFixedSize(120, 30)
        self.comboBoxCryptos.append(comboBoxCrypto)
        
        # fast research among the available pairs
        lineEditCryptoSearch = QtWidgets.QLineEdit()
        lineEditCryptoSearch.setPlaceholderText("")
        
        # add a research function inside the crypto comboBox (pairs of crypto)
        comboBoxCrypto.setLineEdit(lineEditCryptoSearch)

        # add to table
        self.tableCryptoSize.setCellWidget(0, 0, comboBoxCrypto)

        # Field for fees
        labelFees = QtWidgets.QLabel("Fees percentage :")
        self.lineEditFees = QtWidgets.QLineEdit()
        self.lineEditFees.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditFees.setText("0") # default value
        self.lineEditFees.setFixedSize(100, 20)
        
        # push button
        self.buttonOK = QtWidgets.QPushButton('Load Backtest')
        self.buttonOK.clicked.connect(partial(self.checkConditions2Close, tfUnits))
        self.buttonOK.setFixedSize(120, 30)
        self.plusButton = QtWidgets.QPushButton('+')
        self.plusButton.clicked.connect(self.addAsset)
        self.plusButton.setFixedSize(40, 30)
        self.minusButton = QtWidgets.QPushButton('-')
        self.minusButton.clicked.connect(self.removeAsset)
        self.minusButton.setFixedSize(40, 30)
        
        # layout exchange
        layoutExchange = QtWidgets.QVBoxLayout()
        layoutExchange.addWidget(labelExchange)
        layoutExchange.addWidget(self.comboBoxExchange)
        layoutExchange.setAlignment(QtCore.Qt.AlignCenter)

        # layout start date
        layoutStartDate = QtWidgets.QVBoxLayout()
        layoutStartDate.addWidget(labelDate)
        layoutStartDate.addWidget(self.startDate)
        layoutStartDate.setAlignment(QtCore.Qt.AlignCenter)
        
        # Create a horizontal layout (container) to organize Exchange and startDate
        layoutExchDate = QtWidgets.QHBoxLayout()
        layoutExchDate.addLayout(layoutExchange)
        layoutExchDate.addLayout(layoutStartDate)
        layoutExchDate.setAlignment(QtCore.Qt.AlignCenter)
        
        # layout for the timeFrames check boxes
        layoutHTimeframes = QtWidgets.QHBoxLayout()
        for tfUnitIndex in range(len(tfUnits)) :
            layoutHTimeframes.addWidget(self.allCheckBoxes[tfUnitIndex])

        # layout for crypto + size
        layoutCryptoSize = QtWidgets.QHBoxLayout()
        layoutCryptoSize.addWidget(self.tableCryptoSize)
        layoutCryptoSize.setAlignment(QtCore.Qt.AlignCenter)

        # layout for the push buttons
        layoutPush = QtWidgets.QHBoxLayout()
        layoutPush.addWidget(self.minusButton)
        layoutPush.addWidget(self.plusButton)

        # Layout for fees
        layoutFees = QtWidgets.QVBoxLayout()
        layoutFees.addWidget(labelFees)
        layoutFees.addWidget(self.lineEditFees)
        layoutFees.setAlignment(QtCore.Qt.AlignCenter)
        

        # Create a vertical layout to organize all the layouts (crypto and timeframes)
        mainLayoutLeft = QtWidgets.QVBoxLayout()
        mainLayoutRight = QtWidgets.QVBoxLayout()
        mainLayoutDown = QtWidgets.QHBoxLayout()
        mainLayoutUp = QtWidgets.QHBoxLayout()
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayoutLeft.addLayout(layoutExchDate)
        mainLayoutLeft.addLayout(layoutHTimeframes)
        mainLayoutLeft.addLayout(layoutCryptoSize)
        mainLayoutLeft.addLayout(layoutPush)
        mainLayoutLeft.addLayout(layoutFees)

        labelCodeEditor = QtWidgets.QLabel("Python Code For Your Strategy")
        self.editor = CodeEditor()
        self.editor.load_strat_code() 
        self.highlighter = PythonHighlighter(self.editor.document())
        self.saveStrategyButton = QtWidgets.QPushButton('Save Strategy')
        self.saveStrategyButton.setFixedSize(120, 30)
        self.saveStrategyButton.clicked.connect(lambda:self.saveStrategy(strategies_path))
        mainLayoutRight.addWidget(labelCodeEditor, alignment=QtCore.Qt.AlignCenter)
        mainLayoutRight.addWidget(self.editor)
        mainLayoutRight.addWidget(self.saveStrategyButton, alignment=QtCore.Qt.AlignCenter)
        
        mainLayoutUp.addLayout(mainLayoutLeft)
        mainLayoutUp.addLayout(mainLayoutRight)
        mainLayoutDown.addWidget(self.buttonOK,alignment=QtCore.Qt.AlignCenter)
        mainLayout.addLayout(mainLayoutUp)
        mainLayout.addLayout(mainLayoutDown)
        
        # put sub widgets inside the main widget
        self.setLayout(mainLayout)
        self.adjustSize()

    # dynamic adaptation of crypto box to the content of exchange box
    def updateCryptoComboBox(self):
        for pair in self.comboBoxCryptos:
            pair.clear()
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
            for pair in self.comboBoxCryptos:
                pair.addItems(market)
        else :
            for pair in self.comboBoxCryptos:
                pair.addItems(self.markets[self.exchangeName])
            
    def checkConditions2Close(self,tfUnits):
        condition2 = self.comboBoxExchange.currentIndex()>=0
        condition1 = True
        condition3 = True
        condition4 = True
        condition5 = False

        
        def strIsPercent(string):
            if string is not None:
                try:
                    number = float(string.text())
                    if 0<=number and number<=100:
                        return True
                    else:
                        return False
                except ValueError:
                    return False
            return False
        
        if condition1 :
            for row,comboBoxCrypto in enumerate(self.comboBoxCryptos):
                if comboBoxCrypto.findText(comboBoxCrypto.currentText())== -1:
                    condition2 = False
                if not strIsPercent(self.tableCryptoSize.item(row, 1)):
                    condition3 = False
            if condition2 and condition3 :
                if not strIsPercent(self.lineEditFees):
                    condition4 = False
        if condition1 and condition2 and condition3 and condition4:
            for tfUnit in range(len(tfUnits)) :
                if self.allCheckBoxes[tfUnit].isChecked():
                    condition5 = True
                    self.loadNewBackTest(tfUnits)                

    def addAsset(self):
        comboBoxCrypto = QtWidgets.QComboBox()
        comboBoxCrypto.setFixedSize(120, 30)
        lineEditCryptoSearch = QtWidgets.QLineEdit()
        lineEditCryptoSearch.setPlaceholderText("")
        comboBoxCrypto.setLineEdit(lineEditCryptoSearch)
        
        if len(self.markets)!=0:
            comboBoxCrypto.addItems(self.markets[self.exchangeName])

        rowIndex = self.tableCryptoSize.rowCount()
        self.tableCryptoSize.insertRow(rowIndex)

        self.tableCryptoSize.setCellWidget(rowIndex, 0, comboBoxCrypto)
        self.comboBoxCryptos.append(comboBoxCrypto)


    def removeAsset(self):
        lastRowIndex = self.tableCryptoSize.rowCount() - 1
        if lastRowIndex >= 0:
            self.tableCryptoSize.removeRow(lastRowIndex)
            self.comboBoxCryptos = self.comboBoxCryptos[0:len(self.comboBoxCryptos)-1]
        self.tableCryptoSize.setColumnWidth(0, 120)
        
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
        configuration['crypto'] = self.comboBoxCryptos[0].currentText()
        configuration['wallet size'] = [self.tableCryptoSize.item(row, 1).text() for row in range(self.tableCryptoSize.rowCount())]
        configuration['timeframes'] = selectedTf
        configuration['startDate'] = self.startDate.date()
        configuration['stratName'] = self.selectedStrat
        configuration['fees'] = float(self.lineEditFees.text())
        self.emitterInstance.backTestSignal.emit(configuration)

    def updateStrat(self,stratName):
        self.selectedStrat = stratName

    
    def saveStrategy(self,strategies_path):    
        code_content = self.editor.toPlainText()
        strategy_name = (code_content.split('class ')[1]).split('(')[0]
        file_path = os.path.join(strategies_path, f"{strategy_name}.py")
        print(file_path)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code_content)
        
        
