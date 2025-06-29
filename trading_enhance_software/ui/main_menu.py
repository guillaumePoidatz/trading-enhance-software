import os
import sys
from PyQt5 import QtWidgets

from trading_enhance_software.utils.emitter import Emitter
from trading_enhance_software.ui.sidebar import Sidebar
from trading_enhance_software.simulation.backtest import BackTest


class UIMainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.thread_backtest = None
        selected_strat = "BolTrend"

        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        strategies_path = os.path.join(base_path, "strategies")

        # List of the saved strategies
        self.saved_strategies = list()
        try:
            for file in os.listdir(strategies_path):
                if file.endswith(".py"):
                    file_name, _ = os.path.splitext(file)
                    self.saved_strategies.append(file_name)
        except FileNotFoundError as e:
            print(f"Error when accessing {strategies_path}: {e}")
            print(os.listdir(base_path))
            for root, _, files in os.walk(base_path):
                for file in files:
                    print(os.path.join(root, file))

        # for the multithreading
        self.emitter_instance = Emitter()
        self.emitter_instance.backtest_signal.connect(self.launch_backtest)
        self.emitter_instance.backtest_results_window_signal.connect(
            self.show_selection_backtest_window
        )
        self.emitter_instance.display_backtest_window_signal.connect(
            self.show_backtest_window
        )

        # create a menu for the main window
        menubar = self.menuBar()

        # create a scrolling menu "File"
        file_menu = menubar.addMenu("BenchStrat")

        # create an actions inside the scrolling menu "File"
        new_configuration = QtWidgets.QAction("New configuration", self)
        saved_strategy = QtWidgets.QAction("Launch saved strategy", self)

        file_menu.addAction(new_configuration)
        file_menu.addAction(saved_strategy)

        # create a scrolling menu
        saved_strategy.setMenu(self.create_saved_strategy_menu())

        new_configuration.triggered.connect(self.on_config_btn1_toggled)

        self.ui = Sidebar()
        self.ui.setupUi(self, selected_strat, self.emitter_instance, strategies_path)

        self.ui.icon_only_widget.hide()
        # initiate the page
        self.ui.stacked_widget.setCurrentIndex(0)
        self.ui.config_btn1.setChecked(True)

        # connect buttons to the actions they have to process
        self.ui.config_btn1.toggled.connect(self.on_config_btn1_toggled)
        self.ui.rl_btn1.toggled.connect(self.on_rl_btn1_toggled)
        self.ui.select_backtest_btn1.toggled.connect(
            self.on_select_backtest_btn1_toggled
        )
        self.ui.backtest_window_btn1.toggled.connect(self.on_backtest_btn1_toggled)

    ## functions for changing menu page

    def on_config_btn1_toggled(self):
        self.ui.stacked_widget.setCurrentIndex(0)

    def on_rl_btn1_toggled(self):
        self.ui.stacked_widget.setCurrentIndex(1)

    def on_select_backtest_btn1_toggled(self):
        self.ui.stacked_widget.setCurrentIndex(2)

    def on_backtest_btn1_toggled(self):
        self.ui.stacked_widget.setCurrentIndex(3)

    def show_selection_backtest_window(self, results):
        self.ui.selection_backtest_window.update_contents(
            results["df_trades"],
            results["df_backtest"],
            results["general_informations"],
            results["profits_month"],
            results["years"],
            results["selected_crypto"],
            results["timeframe_units"],
        )
        self.ui.stacked_widget.setCurrentIndex(2)

    def show_backtest_window(self, backtest_informations):
        self.ui.backtest_window.update_contents(
            backtest_informations["orderBookHistory"],
            backtest_informations["dfBackTest"],
            backtest_informations["generalInformations"],
            backtest_informations["fontSize"],
            backtest_informations["dateFormat"],
            backtest_informations["years"],
            backtest_informations["profitsMonth"],
        )
        self.ui.backtest_window.setWindowTitle(
            "Backtest "
            + backtest_informations["tfUnit"]
            + " "
            + backtest_informations["crypto"]
            + " strategy"
        )

    # launch the backTest
    def launch_backtest(self, configuration):
        if self.thread_backtest is None or not self.thread_backtest.isRunning():
            self.thread_backtest = BackTest(
                configuration["exchange"],
                configuration["crypto"],
                configuration["timeframes"],
                configuration["startDate"],
                configuration["stratName"],
                configuration["fees"],
                self.emitter_instance,
            )
            self.thread_backtest.start()

    # just a scrolling menu for saved strategies
    def create_saved_strategy_menu(self):
        saved_strategy_menu = QtWidgets.QMenu(self)
        for strategy_name in self.saved_strategies:
            action = QtWidgets.QAction(strategy_name, self)
            action.setProperty("strategyName", strategy_name)
            action.triggered.connect(
                lambda checked, action=action: self.load_strategy(action)
            )
            # add the strategy name to the menu
            saved_strategy_menu.addAction(action)
        return saved_strategy_menu

    # in charge of loading a presaved strategy
    def load_strategy(self, action):
        self.ui.backtest_configuration_page.update_strat(
            action.property("strategyName")
        )
