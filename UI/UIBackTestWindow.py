import pandas as pd
from PyQt5 import QtWidgets,QtCore
from UI.GraphWidget import GraphWidget
from UI.UITabYearWidget import UITabYearWidget

# class to create a window for backtesting trading strategies
class UIBackTestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # configure the BT widget
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)
       
        
    def updateContents(self,orderBookHistory,dfBackTest,generalInformations,fontSize,dateFormat,years,profitsMonth):
        self.orderBookHistory = orderBookHistory
        self.dfBackTest = dfBackTest
        self.generalInformations = generalInformations
        self.fontSize = fontSize
        self.dateFormat = dateFormat
        self.years = years
        self.profitsMonth = profitsMonth

        while self.mainLayout.count():
            child = self.mainLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # -- create the array for general and important informations --
        mainArrayWidget = QtWidgets.QTableWidget()
        mainArrayWidget.setRowCount(len(self.generalInformations.columns))
        mainArrayWidget.setColumnCount(len(self.generalInformations))
        # Put datas in the array
        for i, row in enumerate(self.generalInformations.index):
            rowGeneralInformations = self.generalInformations.iloc[row]
            for j, value in enumerate(rowGeneralInformations):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # alignment (center)
                mainArrayWidget.setItem(i, j, item)

        mainArrayWidget.horizontalHeader().setVisible(False)
        mainArrayWidget.setVerticalHeaderLabels(generalInformations.columns)
        mainArrayWidget.resizeColumnsToContents()
        mainArrayWidget.resizeRowsToContents()
        
        # -- create the array containing all the trade of the backtest -- 
        # create the QTableWidget
        tradeBookWidget = QtWidgets.QTableWidget()

        # configure the array
        tradeBookWidget.setRowCount(len(orderBookHistory))
        tradeBookWidget.setColumnCount(len(orderBookHistory.columns))

        # Put datas in the array
        for i, row in enumerate(self.orderBookHistory.index):
            rowDfBackTest = self.orderBookHistory.iloc[row]
            for j, value in enumerate(rowDfBackTest):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # alignment (center)
                tradeBookWidget.setItem(i, j, item)

        # Replace colonm number by colonm title
        tradeBookWidget.setHorizontalHeaderLabels(self.orderBookHistory.columns)

         # Set cells size
        tradeBookWidget.resizeColumnsToContents()

        # -- Create the Matplotlib graphic for evolution of wallet --
        dateSeries0 = pd.Series([self.dfBackTest['dates'][0]])
        walletSeries0 = pd.Series([self.orderBookHistory['usdt size wallet'][0]])
        
        walletGraph = GraphWidget(
            'plot',
            pd.concat([dateSeries0, self.orderBookHistory['date']]),
            pd.concat([walletSeries0,self.orderBookHistory['usdt size wallet']]),
            'wallet (usdt)',
            self.fontSize,
            self.dateFormat,
            enableZoom = True,
            enablePushMove = True,
            enableCursor = True
            )

        initialWallet = self.orderBookHistory['usdt size wallet'][0]
        initialPrice = self.dfBackTest['close prices'][0]
        walletGraph.addCurve(self.dfBackTest['dates'],self.dfBackTest['close prices'].apply(lambda x: x * initialWallet / initialPrice))
        
        walletGraph.drawRecenterIcon()
        
        # create the vertical layout for the arrays
        arrayLayout = QtWidgets.QVBoxLayout()
        arrayLayout.addWidget(mainArrayWidget)
        arrayLayout.addWidget(tradeBookWidget)
        
        # create the horizontal layout (container) to organize the display of the widgets
        generalBTLayout = QtWidgets.QHBoxLayout()
        generalBTLayout.addWidget(walletGraph.canvas)
        generalBTLayout.addLayout(arrayLayout)

        # create a widget to contain the arrays and graphics (tab)
        tabMain = QtWidgets.QWidget()
        tabYears = []
        tabMain.setLayout(generalBTLayout)

        # Add the tabs to the tab widget
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.addTab(tabMain,'General Informations')
        for index in range(len(years)) :
            tabYearX = UITabYearWidget(self.profitsMonth[years[index][0]],self.fontSize,self.dateFormat)
            tabYears.append(tabYearX)
            tabTitle = 'Informations for ' + str(years[index][0])
            tabWidget.addTab(tabYears[index],tabTitle)

        self.mainLayout.addWidget(tabWidget)
        
        return None



