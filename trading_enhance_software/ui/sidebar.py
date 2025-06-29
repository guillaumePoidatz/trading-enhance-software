from PyQt5 import QtCore, QtGui, QtWidgets
from trading_enhance_software.ui.select_backtest_window import UISelectBackTestWindow
from trading_enhance_software.ui.backtest_window import UIBackTestWindow
from trading_enhance_software.ui.selection_menu import UISelectionMenu
from trading_enhance_software.ui.rl_menu import UIRLMenu


class Sidebar(object):
    def setupUi(self, main_window, selected_strat, emitter_instance, strategies_path):
        self.object_name_string = "BenchStrat"
        main_window.setObjectName(self.object_name_string)
        main_window.resize(950, 600)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        # layout for the main window
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setObjectName("grid_layout")

        # object close side bar
        self.icon_only_widget = QtWidgets.QWidget(self.central_widget)
        self.icon_only_widget.setObjectName("icon_only_widget")

        # main layout for close side bar
        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.vertical_layout_3.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_3.setSpacing(0)
        self.vertical_layout_3.setObjectName("vertical_layout_3")

        # icon SideBar
        self.horizontal_layout_3 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_3.setObjectName("horizontal_layout_3")
        self.side_bar_label1 = QtWidgets.QLabel(self.icon_only_widget)
        self.side_bar_label1.setMinimumSize(QtCore.QSize(50, 50))
        self.side_bar_label1.setMaximumSize(QtCore.QSize(50, 50))
        self.side_bar_label1.setText("")
        self.side_bar_label1.setPixmap(QtGui.QPixmap("UI/icon/Logo.png"))
        self.side_bar_label1.setScaledContents(True)
        self.side_bar_label1.setObjectName("logo_label_1")
        self.horizontal_layout_3.addWidget(self.side_bar_label1)
        self.vertical_layout_3.addLayout(self.horizontal_layout_3)

        # sub layout for all other icon (close side bar)
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setObjectName("vertical_layout")

        # close side bar : icon for the configuration menu
        self.config_btn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.config_btn1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("UI/icon/home-4-32.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon1.addPixmap(
            QtGui.QPixmap("UI/icon/home-4-48.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.config_btn1.setIcon(icon1)
        self.config_btn1.setIconSize(QtCore.QSize(20, 20))
        self.config_btn1.setCheckable(True)
        self.config_btn1.setAutoExclusive(True)
        self.config_btn1.setObjectName("config_btn1")
        self.vertical_layout.addWidget(self.config_btn1)

        # close side bar : icon for the RL-based strategy menu
        self.rl_btn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.rl_btn1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap("UI/icon/product-32.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon2.addPixmap(
            QtGui.QPixmap("UI/icon/product-48.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.rl_btn1.setIcon(icon2)
        self.rl_btn1.setIconSize(QtCore.QSize(20, 20))
        self.rl_btn1.setCheckable(True)
        self.rl_btn1.setAutoExclusive(True)
        self.rl_btn1.setObjectName("rl_btn1")
        self.vertical_layout.addWidget(self.rl_btn1)

        # close side bar : icon for the backTest Menu
        self.select_backtest_btn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.select_backtest_btn1.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap("UI/icon/dashboard-5-32.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon3.addPixmap(
            QtGui.QPixmap("UI/icon/dashboard-5-48.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.select_backtest_btn1.setIcon(icon3)
        self.select_backtest_btn1.setIconSize(QtCore.QSize(20, 20))
        self.select_backtest_btn1.setCheckable(True)
        self.select_backtest_btn1.setAutoExclusive(True)
        self.select_backtest_btn1.setObjectName("select_backtest_btn1")
        self.vertical_layout.addWidget(self.select_backtest_btn1)

        # close side bar : icon for the the monte carlo window
        self.backtest_window_btn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.backtest_window_btn1.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap("UI/icon/activity-feed-32.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon4.addPixmap(
            QtGui.QPixmap("UI/icon/activity-feed-48.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.backtest_window_btn1.setIcon(icon4)
        self.backtest_window_btn1.setIconSize(QtCore.QSize(20, 20))
        self.backtest_window_btn1.setCheckable(True)
        self.backtest_window_btn1.setAutoExclusive(True)
        self.backtest_window_btn1.setObjectName("backtest_window_btn1")
        self.vertical_layout.addWidget(self.backtest_window_btn1)

        # add the sublayout to the layout of the sidebar
        self.vertical_layout_3.addLayout(self.vertical_layout)

        # icon to quit the appli
        spacer_item = QtWidgets.QSpacerItem(
            20,
            375,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.vertical_layout_3.addItem(spacer_item)
        self.exit_btn1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.exit_btn1.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap("UI/icon/close-window-64.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.exit_btn1.setIcon(icon5)
        self.exit_btn1.setIconSize(QtCore.QSize(20, 20))
        self.exit_btn1.setObjectName("exit_btn1")
        self.vertical_layout_3.addWidget(self.exit_btn1)

        # add the close side bar object to the main layout
        self.grid_layout.addWidget(self.icon_only_widget, 0, 0, 1, 1)

        # object for the open sidebar
        self.full_menu_widget = QtWidgets.QWidget(self.central_widget)
        self.full_menu_widget.setObjectName("full_menu_widget")
        # layout for the open sidebar
        self.vertical_layout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.vertical_layout_4.setObjectName("vertical_layout_4")

        # sidebar icon
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2.setSpacing(0)
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")
        self.sidebar_label2 = QtWidgets.QLabel(self.full_menu_widget)
        self.sidebar_label2.setMinimumSize(QtCore.QSize(40, 40))
        self.sidebar_label2.setMaximumSize(QtCore.QSize(40, 40))
        self.sidebar_label2.setText("")
        self.sidebar_label2.setPixmap(QtGui.QPixmap("UI/icon/Logo.png"))
        self.sidebar_label2.setScaledContents(True)
        self.sidebar_label2.setObjectName("sidebar_label2")
        self.horizontal_layout_2.addWidget(self.sidebar_label2)
        self.sidebar_label3 = QtWidgets.QLabel(self.full_menu_widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.sidebar_label3.setFont(font)
        self.sidebar_label3.setObjectName("sidebar_label3")
        self.horizontal_layout_2.addWidget(self.sidebar_label3)
        self.vertical_layout_4.addLayout(self.horizontal_layout_2)

        # sublayout for open sidebar
        self.vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.vertical_layout_2.setSpacing(0)
        self.vertical_layout_2.setObjectName("vertical_layout_2")

        self.config_btn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.config_btn2.setIcon(icon1)
        self.config_btn2.setIconSize(QtCore.QSize(14, 14))
        self.config_btn2.setCheckable(True)
        self.config_btn2.setAutoExclusive(True)
        self.config_btn2.setObjectName("config_btn2")
        self.vertical_layout_2.addWidget(self.config_btn2)

        self.rl_btn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.rl_btn2.setIcon(icon2)
        self.rl_btn2.setIconSize(QtCore.QSize(14, 14))
        self.rl_btn2.setCheckable(True)
        self.rl_btn2.setAutoExclusive(True)
        self.rl_btn2.setObjectName("rl_btn2")
        self.vertical_layout_2.addWidget(self.rl_btn2)

        self.select_backtest_btn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.select_backtest_btn2.setIcon(icon3)
        self.select_backtest_btn2.setIconSize(QtCore.QSize(14, 14))
        self.select_backtest_btn2.setCheckable(True)
        self.select_backtest_btn2.setAutoExclusive(True)
        self.select_backtest_btn2.setObjectName("select_backtest_btn2")
        self.vertical_layout_2.addWidget(self.select_backtest_btn2)

        self.backtest_window_btn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.backtest_window_btn2.setIcon(icon4)
        self.backtest_window_btn2.setIconSize(QtCore.QSize(14, 14))
        self.backtest_window_btn2.setCheckable(True)
        self.backtest_window_btn2.setAutoExclusive(True)
        self.backtest_window_btn2.setObjectName("backtest_window_btn2")
        self.vertical_layout_2.addWidget(self.backtest_window_btn2)

        # add sublayout to the open sidebar main layout
        self.vertical_layout_4.addLayout(self.vertical_layout_2)

        # exit button open side bar
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            373,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.vertical_layout_4.addItem(spacerItem1)
        self.exit_btn2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.exit_btn2.setIcon(icon5)
        self.exit_btn2.setIconSize(QtCore.QSize(14, 14))
        self.exit_btn2.setObjectName("exit_btn2")
        self.vertical_layout_4.addWidget(self.exit_btn2)

        # add the open sidebar object to the main layout
        self.grid_layout.addWidget(self.full_menu_widget, 0, 1, 1, 1)

        #  non side bar object
        self.widget_3 = QtWidgets.QWidget(self.central_widget)
        self.widget_3.setObjectName("widget_3")
        # non side bar layout
        self.vertical_layout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.vertical_layout_5.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_5.setSpacing(0)
        self.vertical_layout_5.setObjectName("vertical_layout_5")

        # header object
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setObjectName("widget")

        # layout for the header
        self.horizontal_layout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontal_layout_4.setContentsMargins(0, 0, 9, 0)
        self.horizontal_layout_4.setSpacing(0)
        self.horizontal_layout_4.setObjectName("horizontal_layout_4")

        # button for opening and closing the side bar
        self.change_btn = QtWidgets.QPushButton(self.widget)
        self.change_btn.setFixedSize(30, 30)
        self.change_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap("UI/icon/menu-4-32.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.change_btn.setIcon(icon6)
        self.change_btn.setIconSize(QtCore.QSize(14, 14))
        self.change_btn.setCheckable(True)
        self.change_btn.setObjectName("change_btn")
        # add the button to the header layout
        self.horizontal_layout_4.addWidget(self.change_btn, 0, QtCore.Qt.AlignLeft)

        # add the header to the non side bar layout
        self.vertical_layout_5.addWidget(self.widget)
        # creation of the main page object
        self.stacked_widget = QtWidgets.QStackedWidget(self.widget_3)
        self.stacked_widget.setObjectName("stacked_widget")

        # BT configuration page
        self.backtest_configuration_page = UISelectionMenu(
            selected_strat, emitter_instance, strategies_path
        )
        self.stacked_widget.addWidget(self.backtest_configuration_page)

        # RL page
        self.rl_page = UIRLMenu(strategies_path)
        self.stacked_widget.addWidget(self.rl_page)

        # BT page
        self.backtest_display = QtWidgets.QWidget()
        backtest_layout = QtWidgets.QVBoxLayout(self.backtest_display)
        self.selection_backtest_window = UISelectBackTestWindow(emitter_instance)
        self.backtest_window = UIBackTestWindow()
        backtest_layout.addWidget(self.selection_backtest_window)
        backtest_layout.addWidget(self.backtest_window)
        self.selection_backtest_window.setFixedHeight(40)
        self.selection_backtest_window.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.selection_backtest_window.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        self.stacked_widget.addWidget(self.backtest_display)

        # Monte Carlo page
        self.monte_carlo_page = QtWidgets.QWidget()
        self.monte_carlo_page.setObjectName("monte_carlo_page")
        self.grid_layout_4 = QtWidgets.QGridLayout(self.monte_carlo_page)
        self.grid_layout_4.setObjectName("grid_layout_4")
        self.label_6 = QtWidgets.QLabel(self.monte_carlo_page)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.grid_layout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.stacked_widget.addWidget(self.monte_carlo_page)

        # add the main page object to the non side bar layout
        self.vertical_layout_5.addWidget(self.stacked_widget)

        # add non side bar object to the layout of the Main Window
        self.grid_layout.addWidget(self.widget_3, 0, 2, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        # connect all the button to the actions they have to proceed
        self.retranslate_ui(main_window)
        self.change_btn.toggled["bool"].connect(self.icon_only_widget.setVisible)  # type: ignore
        self.change_btn.toggled["bool"].connect(self.full_menu_widget.setHidden)  # type: ignore
        self.config_btn1.toggled["bool"].connect(self.config_btn2.setChecked)  # type: ignore
        self.rl_btn1.toggled["bool"].connect(self.rl_btn2.setChecked)
        self.select_backtest_btn1.toggled["bool"].connect(
            self.select_backtest_btn2.setChecked
        )  # type: ignore
        self.backtest_window_btn1.toggled["bool"].connect(
            self.backtest_window_btn2.setChecked
        )  # type: ignore
        self.config_btn2.toggled["bool"].connect(self.config_btn1.setChecked)  # type: ignore
        self.rl_btn2.toggled["bool"].connect(self.rl_btn1.setChecked)
        self.select_backtest_btn2.toggled["bool"].connect(
            self.select_backtest_btn1.setChecked
        )  # type: ignore
        self.backtest_window_btn2.toggled["bool"].connect(
            self.backtest_window_btn1.setChecked
        )  # type: ignore
        self.exit_btn2.clicked.connect(main_window.close)  # type: ignore
        self.exit_btn1.clicked.connect(main_window.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(main_window)

    # function to give a name to all the items for the front-end
    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(
            _translate(self.object_name_string, self.object_name_string)
        )
        self.sidebar_label3.setText(_translate(self.object_name_string, "Sidebar"))
        self.config_btn2.setText(_translate(self.object_name_string, "Configuration"))
        self.rl_btn2.setText(_translate(self.object_name_string, "RL-based strategy"))
        self.select_backtest_btn2.setText(
            _translate(self.object_name_string, "Display BackTest")
        )
        self.backtest_window_btn2.setText(
            _translate(self.object_name_string, "Monte Carlo Simulation")
        )
        self.exit_btn2.setText(_translate(self.object_name_string, "Exit"))
