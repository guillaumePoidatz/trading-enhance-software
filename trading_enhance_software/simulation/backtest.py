from PyQt5.QtCore import QThread
import copy
import datetime as dt
import pandas as pd
from typing import List

from data_mining.data_mining import data_mining
from trading_enhance_software.utils.file_manager import read_json_file
from simulation.analyze_backtest_datas import analyze_backtest_datas


def compute_backtest(
    selected_exchange: str,
    selected_crypto: str,
    timeframe_units: List[str],
    QtPyStartDate,
    strat_name: str,
    fees: float,
):
    """This function responsible of simulating the backtest and to concatenate
    all the assessment metrics of the strategy from the different timeframes

    Args:
        selected_exchange (str): _description_
        selected_crypto (str): _description_
        timeframe_units (List): _description_
        QtPyStartDate (_type_): _description_
        strat_name (str): _description_
        fees (float): _description_

    Returns:
        _type_: _description_
    """
    timeframe = {
        "dates": [],
        "open prices": [],
        "highest prices": [],
        "lowest prices": [],
        "close prices": [],
        "volumes": [],
    }

    crypto = {
        "1w": copy.deepcopy(dict(timeframe)),
        "1d": copy.deepcopy(dict(timeframe)),
        "4h": copy.deepcopy(dict(timeframe)),
        "1h": copy.deepcopy(dict(timeframe)),
        "15m": copy.deepcopy(dict(timeframe)),
        "5m": copy.deepcopy(dict(timeframe)),
    }

    start_date_datetime = dt.datetime(
        QtPyStartDate.year(), QtPyStartDate.month(), QtPyStartDate.day()
    )
    start_date = int(start_date_datetime.timestamp() * 1000)

    file_name = data_mining(
        selected_exchange, selected_crypto, timeframe_units, start_date
    )
    crypto = read_json_file(file_name)
    df_backtest = dict()
    results = dict()

    for timeframe_unit in timeframe_units:
        df_backtest[timeframe_unit] = pd.DataFrame(crypto[timeframe_unit])
        # we start from the start date and we reinitialize the index
        df_backtest[timeframe_unit] = df_backtest[timeframe_unit][
            df_backtest[timeframe_unit]["dates"] >= start_date
        ].reset_index(drop=True)
        df_backtest[timeframe_unit]["dates"] = pd.to_datetime(
            df_backtest[timeframe_unit]["dates"], unit="ms"
        )

    # inital conditions
    initial_usdt = 1000
    initial_coin = 0

    # -- compute the strategy --

    # stock every trades
    df_trades = (
        dict()
    )  # for general informations such as the global evolution of the waller
    years = dict()
    profits_month = dict()
    profits_year = dict()
    # stock the general and important informations
    general_informations = dict()

    # backtest on each wanted dataframe, manage the global backtest
    for timeframe_unit in timeframe_units:
        analyze_backtest_datas(
            timeframe_unit,
            df_backtest,
            general_informations,
            df_trades,
            years,
            initial_usdt,
            initial_coin,
            profits_month,
            profits_year,
            strat_name,
            fees,
        )

    results = {
        "df_trades": df_trades,
        "df_backtest": df_backtest,
        "general_informations": general_informations,
        "profits_month": profits_month,
        "years": years,
        "selected_crypto": selected_crypto,
        "timeframe_units": timeframe_units,
    }

    return results


class BackTest(QThread):
    def __init__(
        self,
        selected_exchange: str,
        selected_crypto: str,
        timeframe_units: List[str],
        start_date,
        strat_name: str,
        fees: float,
        emitter_instance,
    ):
        """Backtest object is managing all the simulation part while the user interface is still working

        Args:
            selected_exchange (str): _description_
            selected_crypto (str): _description_
            timeframe_units (List[str]): _description_
            start_date (_type_): _description_
            strat_name (str): _description_
            fees (float): _description_
            emitter_instance (_type_): _description_
        """
        super().__init__()
        self.selected_exchange = selected_exchange
        self.selected_crypto = selected_crypto
        self.timeframe_units = timeframe_units
        self.start_date = start_date
        self.results = dict()
        self.strat_name = strat_name
        self.fees = fees
        self.emitter_instance = emitter_instance

    def run(self):
        results = compute_backtest(
            self.selected_exchange,
            self.selected_crypto,
            self.timeframe_units,
            self.start_date,
            self.strat_name,
            self.fees,
        )
        self.emitter_instance.backtest_results_window_signal.emit(results)
