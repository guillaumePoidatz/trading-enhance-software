import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from UI.UIBTStrategyMenu import UIBTStrategyMenu
from UI.UISelectBackTestWindow import UISelectBackTestWindow
#from simulation.BackTest import BackTest
from Emitter import Emitter
from UI.SideBarBT import SideBarBT

class UIMainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadBackTest = None
        selectedStrat = 'BolTrend'


        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        strategies_path = os.path.join(base_path, 'strategies')

        # List of the saved strategies
        self.savedStrategies  = list()
        try :
            for file in os.listdir(strategies_path):
                if file.endswith(".py"):
                    fileName, _ = os.path.splitext(file)
                    self.savedStrategies.append(fileName)
        except :
            print(os.listdir(base_path))
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    print(os.path.join(root, file))
                
        # for the multithreading
        self.emitterInstance = Emitter()
        self.emitterInstance.backTestSignal.connect(self.launchBacktest)
        self.emitterInstance.backTestResultsWindowSignal.connect(self.showSelectionBTWindow)
        self.emitterInstance.displayBTWindowSignal.connect(self.showBTWindow)
        
        # create a menu for the main window
        menubar = self.menuBar()

        # create a scrolling menu "File"
        fileMenu = menubar.addMenu('BenchStrat')

        # create an actions inside the scrolling menu "File"
        newConfiguration = QtWidgets.QAction('New configuration', self)
        newBTStrategy = QtWidgets.QAction('New strategy',self)
        savedStrategy = QtWidgets.QAction('Launch saved strategy',self)
        
        fileMenu.addAction(newConfiguration)
        fileMenu.addAction(newBTStrategy)
        fileMenu.addAction(savedStrategy)
        # create a scrolling menu
        savedStrategy.setMenu(self.createSavedStrategyMenu())

        newConfiguration.triggered.connect(self.onConfigBtn1Toggled)
        newBTStrategy.triggered.connect(self.showBTStrategyMenu)

        
        self.ui = SideBarBT()
        self.ui.setupUi(self,selectedStrat,self.emitterInstance)

        self.ui.icon_only_widget.hide()
        # initiate the page
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.configBtn1.setChecked(True)

        # connect buttons to the actions they have to process
        self.ui.configBtn1.toggled.connect(self.onConfigBtn1Toggled)
        self.ui.selectBTbtn1.toggled.connect(self.onSelectBTbtn1Toggled)
        self.ui.BTwindowBtn1.toggled.connect(self.onBTwindowBtn1Toggled)
        
    
    ## Change QPushButton Checkable status when stackedWidget index changed
    def onStackedWidgetCurrentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    ## functions for changing menu page

            
    def onConfigBtn1Toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def onConfigBtn2Toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def onSelectBTbtn1Toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def onSelectBTbtn2Toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def onBTwindowBtn1Toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def onBTwindowBtn2Toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def showSelectionBTWindow(self,results):
        self.ui.selectionBTWindow.updateContents(
            results['dfTrades'],
            results['dfBackTest'],
            results['generalInformations'],
            results['profitsMonth'],
            results['years'],
            results['selectedCrypto'],
            results['timeFrameUnits']
        )
        self.ui.stackedWidget.setCurrentIndex(1)

    def showBTWindow(self,BTInformations):
        self.ui.BTWindow.updateContents(
            BTInformations['orderBookHistory'],
            BTInformations['dfBackTest'],
            BTInformations['generalInformations'],
            BTInformations['fontSize'],
            BTInformations['dateFormat'],
            BTInformations['years'],
            BTInformations['profitsMonth']
            )
        self.ui.BTWindow.setWindowTitle('Backtest '+ BTInformations['tfUnit'] + ' ' + BTInformations['crypto'] + ' strategy')
           
    # launch the backTest
    def launchBacktest(self,configuration):
        if self.threadBackTest is None or not self.threadBackTest.isRunning():
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

    # here the interface to build your own strategy
    def showBTStrategyMenu(self):
        self.BTStrategyMenu = UIBTStrategyMenu(self.emitterInstance)
        self.BTStrategyMenu.exec()

        
    # just a scrolling menu for saved strategies
    def createSavedStrategyMenu(self):
        savedStrategyMenu = QtWidgets.QMenu(self)
        for strategyName in self.savedStrategies:
            action = QtWidgets.QAction(strategyName, self)
            action.setProperty("strategyName", strategyName)
            action.triggered.connect(lambda checked, action=action: self.loadStrategy(action))
            # add the strategy name to the menu
            savedStrategyMenu.addAction(action)
        return savedStrategyMenu

     # in charge of loading a presaved strategy
    def loadStrategy(self,action):
        self.ui.BTconfigurationPage.updateStrat(action.property("strategyName"))

