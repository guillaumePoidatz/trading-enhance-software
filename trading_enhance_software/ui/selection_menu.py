import os
from PyQt5 import QtWidgets, QtCore
from functools import partial

from trading_enhance_software.utils.update_market_thread import UpdateMarketThread
from trading_enhance_software.ui.code_editor import CodeEditor
from trading_enhance_software.ui.highlighter.py_highlight import PythonHighlighter


class UISelectionMenu(QtWidgets.QWidget):
    def __init__(self, selected_strat, emitter_instance, strategies_path):
        super().__init__()
        self.selected_strat = selected_strat

        # configure the main window
        self.setWindowTitle("Select your configuration")

        # combo box for exchange
        self.combo_box_exchange = QtWidgets.QComboBox()

        labelExchange = QtWidgets.QLabel("Select an exchange :")
        self.combo_box_exchange.addItem("binance")
        self.combo_box_exchange.addItem("bitfinex")
        # self.combo_box_exchange.addItem("bitget")
        self.combo_box_exchange.addItem("bybit")
        # self.combo_box_exchange.addItem("cryptocom")
        self.combo_box_exchange.addItem("gate")
        # self.combo_box_exchange.addItem("kraken")
        # self.combo_box_exchange.addItem("kucoin")
        # self.combo_box_exchange.addItem("mexc")
        # self.combo_box_exchange.addItem("okx")

        # to stock the markets of the exchanges that have been selected
        self.markets = dict()

        # dynamic adaptation of this comboBox Menu to the selected exchange and asyn computing
        self.exchange_name = self.combo_box_exchange.currentText()
        self.emitter_instance = emitter_instance
        self.emitter_instance.market_updated_signal.connect(
            self.on_crypto_combo_box_updated
        )
        self.combo_box_exchange.currentTextChanged.connect(self.update_crypto_combo_box)

        # start date
        self.start_date = QtWidgets.QDateEdit()
        label_date = QtWidgets.QLabel("Select a date :")
        # date formatting
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        # default date = current date
        self.start_date.setDate(self.start_date.date().currentDate())

        # timeframe
        timeframe_units = ["5m", "15m", "1h", "4h", "1d", "1w"]
        self.all_check_boxes = [None] * len(timeframe_units)
        for timeframe_unit_index in range(len(timeframe_units)):
            self.checkbox = QtWidgets.QCheckBox(timeframe_units[timeframe_unit_index])
            self.all_check_boxes[timeframe_unit_index] = self.checkbox

        # Field for tab containing cryptos and wallet size dedicated
        self.table_crypto_size = QtWidgets.QTableWidget(1, 2)
        self.table_crypto_size.setColumnWidth(0, 120)
        self.table_crypto_size.verticalHeader().hide()
        self.table_crypto_size.setHorizontalHeaderLabels(["Crypto", "Size (%)"])
        self.table_crypto_size.setFixedSize(220, self.table_crypto_size.height())
        proto_item = QtWidgets.QTableWidgetItem()
        proto_item.setSizeHint(QtCore.QSize(150, 50))
        proto_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_crypto_size.setItemPrototype(proto_item)

        # Field for cryptos
        self.combo_box_cryptos = []
        combo_box_crypto = QtWidgets.QComboBox()
        combo_box_crypto.setFixedSize(120, 30)
        self.combo_box_cryptos.append(combo_box_crypto)

        # fast research among the available pairs
        line_edit_crypto_search = QtWidgets.QLineEdit()
        line_edit_crypto_search.setPlaceholderText("")

        # add a research function inside the crypto comboBox (pairs of crypto)
        combo_box_crypto.setLineEdit(line_edit_crypto_search)

        # add to table
        self.table_crypto_size.setCellWidget(0, 0, combo_box_crypto)

        # Field for fees
        label_fees = QtWidgets.QLabel("Fees percentage :")
        self.line_edit_fees = QtWidgets.QLineEdit()
        self.line_edit_fees.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit_fees.setText("0")  # default value
        self.line_edit_fees.setFixedSize(100, 20)

        # push button
        self.button_ok = QtWidgets.QPushButton("Load Backtest")
        self.button_ok.clicked.connect(
            partial(self.check_conditions_to_close, timeframe_units)
        )
        self.button_ok.setFixedSize(120, 30)
        self.plus_button = QtWidgets.QPushButton("+")
        self.plus_button.clicked.connect(self.add_asset)
        self.plus_button.setFixedSize(40, 30)
        self.minus_button = QtWidgets.QPushButton("-")
        self.minus_button.clicked.connect(self.remove_asset)
        self.minus_button.setFixedSize(40, 30)

        # layout exchange
        layout_exchange = QtWidgets.QVBoxLayout()
        layout_exchange.addWidget(labelExchange)
        layout_exchange.addWidget(self.combo_box_exchange)
        layout_exchange.setAlignment(QtCore.Qt.AlignCenter)

        # layout start date
        layout_start_date = QtWidgets.QVBoxLayout()
        layout_start_date.addWidget(label_date)
        layout_start_date.addWidget(self.start_date)
        layout_start_date.setAlignment(QtCore.Qt.AlignCenter)

        # Create a horizontal layout (container) to organize Exchange and start_date
        layout_exchange_date = QtWidgets.QHBoxLayout()
        layout_exchange_date.addLayout(layout_exchange)
        layout_exchange_date.addLayout(layout_start_date)
        layout_exchange_date.setAlignment(QtCore.Qt.AlignCenter)

        # layout for the timeFrames check boxes
        layout_horizontal_timeframes = QtWidgets.QHBoxLayout()
        for timeframe_unit_index in range(len(timeframe_units)):
            layout_horizontal_timeframes.addWidget(
                self.all_check_boxes[timeframe_unit_index]
            )

        # layout for crypto + size
        layout_crypto_size = QtWidgets.QHBoxLayout()
        layout_crypto_size.addWidget(self.table_crypto_size)
        layout_crypto_size.setAlignment(QtCore.Qt.AlignCenter)

        # layout for the push buttons
        layout_push = QtWidgets.QHBoxLayout()
        layout_push.addWidget(self.minus_button)
        layout_push.addWidget(self.plus_button)

        # Layout for fees
        layout_fees = QtWidgets.QVBoxLayout()
        layout_fees.addWidget(label_fees)
        layout_fees.addWidget(self.line_edit_fees)
        layout_fees.setAlignment(QtCore.Qt.AlignCenter)

        # Create a vertical layout to organize all the layouts (crypto and timeframes)
        main_layout_left = QtWidgets.QVBoxLayout()
        main_layout_right = QtWidgets.QVBoxLayout()
        main_layout_down = QtWidgets.QHBoxLayout()
        main_layout_up = QtWidgets.QHBoxLayout()
        main_layout = QtWidgets.QVBoxLayout()
        main_layout_left.addLayout(layout_exchange_date)
        main_layout_left.addLayout(layout_horizontal_timeframes)
        main_layout_left.addLayout(layout_crypto_size)
        main_layout_left.addLayout(layout_push)
        main_layout_left.addLayout(layout_fees)

        label_code_editor = QtWidgets.QLabel("Python Code For Your Strategy")
        self.editor = CodeEditor()
        self.editor.load_strat_code()
        self.highlighter = PythonHighlighter(self.editor.document())
        self.save_strategy_button = QtWidgets.QPushButton("Save Strategy")
        self.save_strategy_button.setFixedSize(120, 30)
        self.save_strategy_button.clicked.connect(
            lambda: self.saveStrategy(strategies_path)
        )
        main_layout_right.addWidget(label_code_editor, alignment=QtCore.Qt.AlignCenter)
        main_layout_right.addWidget(self.editor)
        main_layout_right.addWidget(
            self.save_strategy_button, alignment=QtCore.Qt.AlignCenter
        )

        main_layout_up.addLayout(main_layout_left)
        main_layout_up.addLayout(main_layout_right)
        main_layout_down.addWidget(self.button_ok, alignment=QtCore.Qt.AlignCenter)
        main_layout.addLayout(main_layout_up)
        main_layout.addLayout(main_layout_down)

        # put sub widgets inside the main widget
        self.setLayout(main_layout)
        self.adjustSize()

    # dynamic adaptation of crypto box to the content of exchange box
    def update_crypto_combo_box(self):
        for pair in self.combo_box_cryptos:
            pair.clear()
        self.exchange_name = self.combo_box_exchange.currentText()

        # for a new exchange, we have to retrieve the market
        if self.exchange_name not in self.markets.keys():
            self.thread_selected_exchange = UpdateMarketThread(
                self.exchange_name, self.emitter_instance
            )
            self.thread_selected_exchange.start()
        # otherwise we take the recorded market
        else:
            self.on_crypto_combo_box_updated(self.markets[self.exchange_name])

    def on_crypto_combo_box_updated(self, market):
        if self.exchange_name not in self.markets.keys():
            # sort the market pairs
            market.sort()
            # record the available market for this exchange
            self.markets[self.exchange_name] = market
            # add the market to the UI
            for pair in self.combo_box_cryptos:
                pair.addItems(market)
        else:
            for pair in self.combo_box_cryptos:
                pair.addItems(self.markets[self.exchange_name])

    def check_conditions_to_close(self, timeframe_units):
        condition2 = self.combo_box_exchange.currentIndex() >= 0
        condition1 = True
        condition3 = True
        condition4 = True

        def string_is_percent(string):
            if string is not None:
                try:
                    number = float(string.text())
                    if 0 <= number and number <= 100:
                        return True
                    else:
                        return False
                except ValueError:
                    return False
            return False

        if condition1:
            for row, combo_box_crypto in enumerate(self.combo_box_cryptos):
                if combo_box_crypto.findText(combo_box_crypto.currentText()) == -1:
                    condition2 = False
                if not string_is_percent(self.table_crypto_size.item(row, 1)):
                    condition3 = False
            if condition2 and condition3:
                if not string_is_percent(self.line_edit_fees):
                    condition4 = False
        if condition1 and condition2 and condition3 and condition4:
            for tfUnit in range(len(timeframe_units)):
                if self.all_check_boxes[tfUnit].isChecked():
                    self.load_new_backtest(timeframe_units)

    def add_asset(self):
        combo_box_crypto = QtWidgets.QComboBox()
        combo_box_crypto.setFixedSize(120, 30)
        line_edit_crypto_search = QtWidgets.QLineEdit()
        line_edit_crypto_search.setPlaceholderText("")
        combo_box_crypto.setLineEdit(line_edit_crypto_search)

        if len(self.markets) != 0:
            combo_box_crypto.addItems(self.markets[self.exchange_name])

        rowIndex = self.table_crypto_size.rowCount()
        self.table_crypto_size.insertRow(rowIndex)

        self.table_crypto_size.setCellWidget(rowIndex, 0, combo_box_crypto)
        self.combo_box_cryptos.append(combo_box_crypto)

    def remove_asset(self):
        last_row_index = self.table_crypto_size.rowCount() - 1
        if last_row_index >= 0:
            self.table_crypto_size.removeRow(last_row_index)
            self.combo_box_cryptos = self.combo_box_cryptos[
                0 : len(self.combo_box_cryptos) - 1
            ]
        self.table_crypto_size.setColumnWidth(0, 120)

    # load a new configurations if all the conditions are verified
    def load_new_backtest(self, timeframe_units):
        selected_timeframe = []
        configuration = dict()

        # -- check all the state of all the checkboxes --
        # timeframe
        for timeframe_unit in range(len(timeframe_units)):
            if self.all_check_boxes[timeframe_unit].isChecked():
                selected_timeframe.append(timeframe_units[timeframe_unit])

        # configuration
        configuration["exchange"] = self.combo_box_exchange.currentText()
        configuration["crypto"] = self.combo_box_cryptos[0].currentText()
        configuration["wallet size"] = [
            self.table_crypto_size.item(row, 1).text()
            for row in range(self.table_crypto_size.rowCount())
        ]
        configuration["timeframes"] = selected_timeframe
        configuration["startDate"] = self.start_date.date()
        configuration["stratName"] = self.selected_strat
        configuration["fees"] = float(self.line_edit_fees.text())
        self.emitter_instance.backtest_signal.emit(configuration)

    def update_strat(self, strat_name):
        self.selected_strat = strat_name

    def save_strategy(self, strategies_path):
        code_content = self.editor.toPlainText()
        strategy_name = (code_content.split("class ")[1]).split("(")[0]
        file_path = os.path.join(strategies_path, f"{strategy_name}.py")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code_content)
