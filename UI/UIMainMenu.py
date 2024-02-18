import os
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5.QtCore import pyqtSignal

from UI.UISelectionMenu import UISelectionMenu
from UI.UIBTStrategyMenu import UIBTStrategyMenu
from UI.UISelectBackTestWindow import UISelectBackTestWindow
from simulation.BackTest import BackTest
from Emitter import Emitter

class UIMainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedStrat = 'BolTrend'

        # List of the saved strategies
        self.savedStrategies  = list()
        for file in os.listdir("strategies"):
            if file.endswith(".py"):
                fileName, _ = os.path.splitext(file)
                self.savedStrategies.append(fileName)
                
        # for the multithreading
        self.emitterInstance = Emitter()
        self.emitterInstance.backTestSignal.connect(self.launchBacktest)
        self.emitterInstance.backTestResultsWindowSignal.connect(self.showSelectionBTWindow)
        
        # create a menu for the main window
        menubar = self.menuBar()

        # create a scrolling menu "File"
        fileMenu = menubar.addMenu('File')

        # create an actions inside the scrolling menu "File"
        newConfiguration = QAction('New configuration', self)
        newBTStrategy = QAction('New strategy',self)
        savedStrategy = QAction('Launch saved strategy',self)
        
        fileMenu.addAction(newConfiguration)
        fileMenu.addAction(newBTStrategy)
        fileMenu.addAction(savedStrategy)
        # create a scrolling menu
        savedStrategy.setMenu(self.createSavedStrategyMenu())

        newConfiguration.triggered.connect(self.showSelectionMenu)
        newBTStrategy.triggered.connect(self.showBTStrategyMenu)

        self.setWindowTitle('Main Menu')

    # launch the backTest
    def launchBacktest(self,configuration):
        self.threadBackTest = BackTest(
            configuration['exchange'],
            configuration['crypto'],
            configuration['timeframes'],
            configuration['startDate'],
            configuration['stratName'],
            configuration['fees'],
            self.emitterInstance
            )
        self.threadBackTest.start()

    def showSelectionBTWindow(self,results):
        self.selectionBTWindow = UISelectBackTestWindow(
            results['dfTrades'],
            results['dfBackTest'],
            results['generalInformations'],
            results['profitsMonth'],
            results['years'],
            results['selectedCrypto'],
            results['timeFrameUnits']
            )
        self.selectionBTWindow.show()

    # if we select new configuration :
    def showSelectionMenu(self):
        # inside there is a function to emit the backtest signal
        self.selectionMenu = UISelectionMenu(self.selectedStrat,self.emitterInstance)
        self.selectionMenu.exec()

    # here the interface to build your own strategy
    def showBTStrategyMenu(self):
        self.BTStrategyMenu = UIBTStrategyMenu(self.emitterInstance)
        self.BTStrategyMenu.exec()

        
    # just a scrolling menu for saved strategies
    def createSavedStrategyMenu(self):
        savedStrategyMenu = QMenu(self)
        for strategyName in self.savedStrategies:
            action = QAction(strategyName, self)
            action.setProperty("strategyName", strategyName)
            action.triggered.connect(lambda checked, action=action: self.loadStrategy(action))
            # add the strategy name to the menu
            savedStrategyMenu.addAction(action)
        return savedStrategyMenu

     # in charge of loading a presaved strategy
    def loadStrategy(self,action):
        self.selectedStrat = action.property("strategyName")
