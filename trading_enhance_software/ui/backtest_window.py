import pandas as pd
from PyQt5 import QtWidgets, QtCore
from trading_enhance_software.ui.graph_widget import GraphWidget
from trading_enhance_software.ui.tab_year_widget import UITabYearWidget


# class to create a window for backtesting trading strategies
class UIBackTestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # configure the BT widget
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.main_layout)

    def update_contents(
        self,
        order_book_history,
        df_backtest,
        general_informations,
        font_size,
        date_format,
        years,
        profits_month,
    ):
        self.order_book_history = order_book_history
        self.df_backtest = df_backtest
        self.general_informations = general_informations
        self.font_size = font_size
        self.date_format = date_format
        self.years = years
        self.profits_month = profits_month

        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # -- create the array for general and important informations --
        main_array_widget = QtWidgets.QTableWidget()
        main_array_widget.setRowCount(len(self.general_informations.columns))
        main_array_widget.setColumnCount(len(self.general_informations))
        # Put datas in the array
        for i, row in enumerate(self.general_informations.index):
            row_general_informations = self.general_informations.iloc[row]
            for j, value in enumerate(row_general_informations):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # alignment (center)
                main_array_widget.setItem(i, j, item)

        main_array_widget.horizontalHeader().setVisible(False)
        main_array_widget.setVerticalHeaderLabels(general_informations.columns)
        main_array_widget.resizeColumnsToContents()
        main_array_widget.resizeRowsToContents()

        # -- create the array containing all the trade of the backtest --
        # create the QTableWidget
        trade_book_widget = QtWidgets.QTableWidget()

        # configure the array
        trade_book_widget.setRowCount(len(order_book_history))
        trade_book_widget.setColumnCount(len(order_book_history.columns))

        # Put datas in the array
        for i, row in enumerate(self.order_book_history.index):
            row_df_backtest = self.order_book_history.iloc[row]
            for j, value in enumerate(row_df_backtest):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # alignment (center)
                trade_book_widget.setItem(i, j, item)

        # Replace colonm number by colonm title
        trade_book_widget.setHorizontalHeaderLabels(self.order_book_history.columns)

        # Set cells size
        trade_book_widget.resizeColumnsToContents()

        # -- Create the Matplotlib graphic for evolution of wallet --
        date_series0 = pd.Series([self.df_backtest["dates"][0]])
        wallet_series0 = pd.Series([self.order_book_history["usdt size wallet"][0]])

        wallet_graph = GraphWidget(
            "plot",
            pd.concat([date_series0, self.order_book_history["date"]]),
            pd.concat([wallet_series0, self.order_book_history["usdt size wallet"]]),
            "wallet (usdt)",
            self.font_size,
            self.date_format,
            enable_zoom=True,
            enable_push_move=True,
            enable_cursor=True,
        )

        initial_wallet = self.order_book_history["usdt size wallet"][0]
        initial_price = self.df_backtest["close prices"][0]
        wallet_graph.add_curve(
            self.df_backtest["dates"],
            self.df_backtest["close prices"].apply(
                lambda x: x * initial_wallet / initial_price
            ),
        )

        wallet_graph.drawRecenterIcon()

        # create the vertical layout for the arrays
        array_layout = QtWidgets.QVBoxLayout()
        array_layout.addWidget(main_array_widget)
        array_layout.addWidget(trade_book_widget)

        # create the horizontal layout (container) to organize the display of the widgets
        general_backtest_layout = QtWidgets.QHBoxLayout()
        general_backtest_layout.addWidget(wallet_graph.canvas)
        general_backtest_layout.addLayout(array_layout)

        # create a widget to contain the arrays and graphics (tab)
        tab_main = QtWidgets.QWidget()
        tab_years = []
        tab_main.setLayout(general_backtest_layout)

        # Add the tabs to the tab widget
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.addTab(tab_main, "General Informations")
        for index in range(len(years)):
            tabYearX = UITabYearWidget(
                self.profits_month[years[index][0]], self.font_size, self.date_format
            )
            tab_years.append(tabYearX)
            tab_title = "Informations for " + str(years[index][0])
            tab_widget.addTab(tab_years[index], tab_title)

        self.main_layout.addWidget(tab_widget)

        return None
