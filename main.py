# installing venv : python3 -m venv Documents/VENV/BackTestV3
# source Documents/VENV/BackTestV3/bin/activate
# then
# cd Documents/VENV/BackTestV3
# and finally
# python3 main.py


import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

from UI.UIMainMenu import UIMainMenu
from Emitter import Emitter


# create PyQt interface
app = QApplication(sys.argv)
# create main window
mainMenu = UIMainMenu()
# display window
mainMenu.show()
# exec PyQt interface
app.exec_()
    

