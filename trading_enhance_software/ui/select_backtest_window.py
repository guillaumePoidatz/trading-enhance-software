from PyQt5 import QtWidgets, QtCore


class UISelectBackTestWindow(QtWidgets.QWidget):
    def __init__(self, emitter_instance):
        super().__init__()

        self.emitter_instance = emitter_instance
        # configure the layout
        self.setWindowTitle("Select Backtest Window")
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.main_layout)

    def action(self, timeframe_unit):
        backtest_informations = {
            "orderBookHistory": self.order_book_history[timeframe_unit],
            "dfBackTest": self.df_backtest[timeframe_unit],
            "generalInformations": self.general_informations[timeframe_unit],
            "fontSize": 8,
            "dateFormat": "%Y-%m-%d",
            "years": self.years[timeframe_unit],
            "profitsMonth": self.profits_month[timeframe_unit],
            "tfUnit": timeframe_unit,
            "crypto": self.crypto,
        }
        self.emitter_instance.display_backtest_window_signal.emit(backtest_informations)

    def update_contents(
        self,
        order_book_history,
        df_backtest,
        general_informations,
        profits_month,
        years,
        crypto,
        activeTf,
    ):
        self.order_book_history = order_book_history
        self.df_backtest = df_backtest
        self.general_informations = general_informations
        self.profits_month = profits_month
        self.years = years
        self.crypto = crypto
        self.activeTf = activeTf

        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # create QPushButtons
        for timeframe_unit in self.activeTf:
            if not order_book_history[timeframe_unit].empty:
                q_btn = QtWidgets.QPushButton()
                q_btn.setText("Back Testing timeframe " + timeframe_unit)
                q_btn.clicked.connect(
                    lambda checked, unit=timeframe_unit: self.action(unit)
                )
                self.main_layout.addWidget(q_btn)
