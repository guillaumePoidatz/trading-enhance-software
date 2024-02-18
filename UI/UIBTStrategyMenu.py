from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QFont
from PyQt5.Qsci import *

class UIBTStrategyMenu(QDialog):
    def __init__(self,emitterInstance):
        super().__init__()
        self.emitterInstance = emitterInstance
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Python Code For Your Strategy")
        self.resize(1300,900)

        self.setStyleSheet(open("css/style.qss","r").read())
        
        self.windowFont = QFont("Fire Code") # add font for python editor
        self.windowFont.setPointSize(16)
        self.setFont(self.windowFont)

        self.setUpMenu()
        self.setUpBody()

        self.show()

    def get_editor(self):
        pass
    
    def setUpMenu(self):
        pass

    def setUpBody(self):
        pass
