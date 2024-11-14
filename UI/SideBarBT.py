from PyQt5 import QtCore, QtGui, QtWidgets
from UI.UISelectBackTestWindow import UISelectBackTestWindow
from UI.UIBackTestWindow import UIBackTestWindow
from UI.UISelectionMenu import UISelectionMenu
from UI.UIRLMenu import UIRLMenu

class SideBarBT(object):

    def setupUi(self, MainWindow,selectedStrat,emitterInstance,strategies_path):
        
        self.ObjectNameString = "BenchStrat"
        MainWindow.setObjectName(self.ObjectNameString)
        MainWindow.resize(950, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # layout for the main window
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        # object close side bar
        self.icon_only_widget = QtWidgets.QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName("icon_only_widget")

        # main layout for close side bar
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # icon SideBar
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")    
        self.sideBarLabel1 = QtWidgets.QLabel(self.icon_only_widget)
        self.sideBarLabel1.setMinimumSize(QtCore.QSize(50, 50))
        self.sideBarLabel1.setMaximumSize(QtCore.QSize(50, 50))
        self.sideBarLabel1.setText("")
        self.sideBarLabel1.setPixmap(QtGui.QPixmap("UI/icon/Logo.png"))
        self.sideBarLabel1.setScaledContents(True)
        self.sideBarLabel1.setObjectName("logo_label_1")
        self.horizontalLayout_3.addWidget(self.sideBarLabel1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        # sub layout for all other icon (close side bar)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        # close side bar : icon for the configuration menu 
        self.configBtn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.configBtn1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("UI/icon/home-4-32.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon1.addPixmap(QtGui.QPixmap("UI/icon/home-4-48.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.configBtn1.setIcon(icon1)
        self.configBtn1.setIconSize(QtCore.QSize(20, 20))
        self.configBtn1.setCheckable(True)
        self.configBtn1.setAutoExclusive(True)
        self.configBtn1.setObjectName("configBtn1")
        self.verticalLayout.addWidget(self.configBtn1)

        # close side bar : icon for the RL-based strategy menu
        self.RLBtn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.RLBtn1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("UI/icon/product-32.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon2.addPixmap(QtGui.QPixmap("UI/icon/product-48.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.RLBtn1.setIcon(icon2)
        self.RLBtn1.setIconSize(QtCore.QSize(20, 20))
        self.RLBtn1.setCheckable(True)
        self.RLBtn1.setAutoExclusive(True)
        self.RLBtn1.setObjectName("RLBtn1")
        self.verticalLayout.addWidget(self.RLBtn1)

        # close side bar : icon for the backTest Menu
        self.selectBTbtn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.selectBTbtn1.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("UI/icon/dashboard-5-32.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon3.addPixmap(QtGui.QPixmap("UI/icon/dashboard-5-48.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.selectBTbtn1.setIcon(icon3)
        self.selectBTbtn1.setIconSize(QtCore.QSize(20, 20))
        self.selectBTbtn1.setCheckable(True)
        self.selectBTbtn1.setAutoExclusive(True)
        self.selectBTbtn1.setObjectName("selectBTbtn1")
        self.verticalLayout.addWidget(self.selectBTbtn1)

        # close side bar : icon for the the monte carlo window
        self.BTwindowBtn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.BTwindowBtn1.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("UI/icon/activity-feed-32.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon4.addPixmap(QtGui.QPixmap("UI/icon/activity-feed-48.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.BTwindowBtn1.setIcon(icon4)
        self.BTwindowBtn1.setIconSize(QtCore.QSize(20, 20))
        self.BTwindowBtn1.setCheckable(True)
        self.BTwindowBtn1.setAutoExclusive(True)
        self.BTwindowBtn1.setObjectName("BTwindowBtn1")
        self.verticalLayout.addWidget(self.BTwindowBtn1)

        # add the sublayout to the layout of the sidebar
        self.verticalLayout_3.addLayout(self.verticalLayout)

        # icon to quit the appli
        spacerItem = QtWidgets.QSpacerItem(20, 375, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.exitBtn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.exitBtn1.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("UI/icon/close-window-64.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.exitBtn1.setIcon(icon5)
        self.exitBtn1.setIconSize(QtCore.QSize(20, 20))
        self.exitBtn1.setObjectName("exitBtn1")
        self.verticalLayout_3.addWidget(self.exitBtn1)

        # add the close side bar object to the main layout 
        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)

        # object for the open sidebar
        self.full_menu_widget = QtWidgets.QWidget(self.centralwidget)
        self.full_menu_widget.setObjectName("full_menu_widget")
        # layout for the open sidebar
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # sidebar icon
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")  
        self.sideBarLabel2 = QtWidgets.QLabel(self.full_menu_widget)
        self.sideBarLabel2.setMinimumSize(QtCore.QSize(40, 40))
        self.sideBarLabel2.setMaximumSize(QtCore.QSize(40, 40))
        self.sideBarLabel2.setText("")
        self.sideBarLabel2.setPixmap(QtGui.QPixmap("UI/icon/Logo.png"))
        self.sideBarLabel2.setScaledContents(True)
        self.sideBarLabel2.setObjectName("sideBarLabel2")
        self.horizontalLayout_2.addWidget(self.sideBarLabel2)
        self.sideBarLabel3 = QtWidgets.QLabel(self.full_menu_widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.sideBarLabel3.setFont(font)
        self.sideBarLabel3.setObjectName("sideBarLabel3")
        self.horizontalLayout_2.addWidget(self.sideBarLabel3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        # sublayout for open sidebar 
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.configBtn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.configBtn2.setIcon(icon1)
        self.configBtn2.setIconSize(QtCore.QSize(14, 14))
        self.configBtn2.setCheckable(True)
        self.configBtn2.setAutoExclusive(True)
        self.configBtn2.setObjectName("configBtn2")
        self.verticalLayout_2.addWidget(self.configBtn2)

        self.RLBtn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.RLBtn2.setIcon(icon2)
        self.RLBtn2.setIconSize(QtCore.QSize(14, 14))
        self.RLBtn2.setCheckable(True)
        self.RLBtn2.setAutoExclusive(True)
        self.RLBtn2.setObjectName("RLBtn2")
        self.verticalLayout_2.addWidget(self.RLBtn2)

        self.selectBTbtn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.selectBTbtn2.setIcon(icon3)
        self.selectBTbtn2.setIconSize(QtCore.QSize(14, 14))
        self.selectBTbtn2.setCheckable(True)
        self.selectBTbtn2.setAutoExclusive(True)
        self.selectBTbtn2.setObjectName("selectBTbtn2")
        self.verticalLayout_2.addWidget(self.selectBTbtn2)

        self.BTwindowBtn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.BTwindowBtn2.setIcon(icon4)
        self.BTwindowBtn2.setIconSize(QtCore.QSize(14, 14))
        self.BTwindowBtn2.setCheckable(True)
        self.BTwindowBtn2.setAutoExclusive(True)
        self.BTwindowBtn2.setObjectName("BTwindowBtn2")
        self.verticalLayout_2.addWidget(self.BTwindowBtn2)

        # add sublayout to the open sidebar main layout
        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        # exit button open side bar
        spacerItem1 = QtWidgets.QSpacerItem(20, 373, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.exitBtn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.exitBtn2.setIcon(icon5)
        self.exitBtn2.setIconSize(QtCore.QSize(14, 14))
        self.exitBtn2.setObjectName("exitBtn2")
        self.verticalLayout_4.addWidget(self.exitBtn2)

        # add the open sidebar object to the main layout
        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)

        #  non side bar object
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        # non side bar layout
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # header object
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setObjectName("widget")

        # layout for the header
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 9, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        # button for opening and closing the side bar
        self.changeBtn = QtWidgets.QPushButton(self.widget)
        self.changeBtn.setFixedSize(30, 30)
        self.changeBtn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("UI/icon/menu-4-32.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.changeBtn.setIcon(icon6)
        self.changeBtn.setIconSize(QtCore.QSize(14, 14))
        self.changeBtn.setCheckable(True)
        self.changeBtn.setObjectName("changeBtn")
        # add the button to the header layout
        self.horizontalLayout_4.addWidget(self.changeBtn,0,QtCore.Qt.AlignLeft)

        # add the header to the non side bar layout
        self.verticalLayout_5.addWidget(self.widget)
        # creation of the main page object
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_3)
        self.stackedWidget.setObjectName("stackedWidget")

        # BT configuration page
        self.BTconfigurationPage = UISelectionMenu(selectedStrat,emitterInstance,strategies_path)
        self.stackedWidget.addWidget(self.BTconfigurationPage)

        # RL page
        self.RLPage = UIRLMenu()
        self.stackedWidget.addWidget(self.RLPage)

        # BT page
        self.BTDisplay = QtWidgets.QWidget()
        BTLayout = QtWidgets.QVBoxLayout(self.BTDisplay)
        self.selectionBTWindow = UISelectBackTestWindow(emitterInstance)
        self.BTWindow = UIBackTestWindow()
        BTLayout.addWidget(self.selectionBTWindow)
        BTLayout.addWidget(self.BTWindow)
        self.selectionBTWindow.setFixedHeight(40)
        self.selectionBTWindow.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.MinimumExpanding)
        self.selectionBTWindow.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.MinimumExpanding)
        self.stackedWidget.addWidget(self.BTDisplay)

        # Monte Carlo page
        self.MCpage = QtWidgets.QWidget()
        self.MCpage.setObjectName("MCpage")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.MCpage)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_6 = QtWidgets.QLabel(self.MCpage)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.MCpage)

        # add the main page object to the non side bar layout
        self.verticalLayout_5.addWidget(self.stackedWidget)

        # add non side bar object to the layout of the Main Window
        self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        # connect all the button to the actions they have to proceed
        self.retranslateUi(MainWindow) 
        self.changeBtn.toggled['bool'].connect(self.icon_only_widget.setVisible) # type: ignore
        self.changeBtn.toggled['bool'].connect(self.full_menu_widget.setHidden) # type: ignore
        self.configBtn1.toggled['bool'].connect(self.configBtn2.setChecked) # type: ignore
        self.RLBtn1.toggled['bool'].connect(self.RLBtn2.setChecked)
        self.selectBTbtn1.toggled['bool'].connect(self.selectBTbtn2.setChecked) # type: ignore
        self.BTwindowBtn1.toggled['bool'].connect(self.BTwindowBtn2.setChecked) # type: ignore
        self.configBtn2.toggled['bool'].connect(self.configBtn1.setChecked) # type: ignore
        self.RLBtn2.toggled['bool'].connect(self.RLBtn1.setChecked)
        self.selectBTbtn2.toggled['bool'].connect(self.selectBTbtn1.setChecked) # type: ignore
        self.BTwindowBtn2.toggled['bool'].connect(self.BTwindowBtn1.setChecked) # type: ignore
        self.exitBtn2.clicked.connect(MainWindow.close) # type: ignore
        self.exitBtn1.clicked.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # function to give a name to all the items for the front-end
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(self.ObjectNameString, self.ObjectNameString))
        self.sideBarLabel3.setText(_translate(self.ObjectNameString, "Sidebar"))
        self.configBtn2.setText(_translate(self.ObjectNameString, "Configuration"))
        self.RLBtn2.setText(_translate(self.ObjectNameString, "RL-based strategy"))
        self.selectBTbtn2.setText(_translate(self.ObjectNameString, "Display BackTest"))
        self.BTwindowBtn2.setText(_translate(self.ObjectNameString, "Monte Carlo Simulation"))
        self.exitBtn2.setText(_translate(self.ObjectNameString, "Exit"))
            
