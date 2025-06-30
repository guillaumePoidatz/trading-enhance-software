# installing venv : python3 -m venv Documents/VENV/BackTest
# source Documents/VENV/BackTest/bin/activate
# then
# cd Documents/VENV/BackTest
# and finally
# python3 main.py


import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream
from trading_enhance_software.ui.main_menu import UIMainMenu


def resize_to_screen(menu):
    screen_geometry = QApplication.desktop().availableGeometry()
    menu.setGeometry(screen_geometry)


if __name__ == "__main__":
    # create PyQt interface
    app = QApplication(sys.argv)

    ## loading style file
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    css_path = os.path.join(base_path, "css/style.qss")

    style_file = QFile(css_path)
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())
    # create main window
    main_menu = UIMainMenu()
    resize_to_screen(main_menu)
    # display window
    main_menu.show()
    # exec PyQt interface
    app.exec_()
