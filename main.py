# installing venv : python3 -m venv Documents/VENV/BackTest
# source Documents/VENV/BackTestV3/bin/activate
# then
# cd Documents/VENV/BackTest
# and finally
# python3 main.py


import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream
from UI.UIMainMenu import UIMainMenu

def resize2screen(menu):
    screenGeometry = QApplication.desktop().availableGeometry()
    menu.setGeometry(screenGeometry)

if __name__ == "__main__":
    # create PyQt interface
    app = QApplication(sys.argv)
    ## loading style file, Example 2
    style_file = QFile("css/style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())
    # create main window
    mainMenu = UIMainMenu()
    resize2screen(mainMenu)
    # display window
    mainMenu.show()
    # exec PyQt interface
    app.exec_()
    

