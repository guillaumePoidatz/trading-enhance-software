import copy
import ccxt
import os
from data_mining.from_exc_to_raw_data_structure import from_exc_to_raw_data_structure
from trading_enhance_software.utils.file_manager import read_json_file
from utils.file_manager import save_json_file


def data_mining(exchange_name, symbol_name, timeframe, start_date):
    """This function is collecting data on a defined crypto exchange for one crypto pair

    Args:
        exchange_name (_type_): _description_
        symbol_name (_type_): _description_
        timeframe (_type_): _description_
        start_date (_type_): _description_

    Returns:
        _type_: the json file containing the data with this structure:

        {timeframe: {
                    "dates": [],
                    "open prices": [],
                    "highest prices": [],
                    "lowest prices": [],
                    "close prices": [],
                    "volumes": [],
                    },
        }
    """
    exchange_class = getattr(ccxt, exchange_name)
    exch = exchange_class({})  #'timeout': 100000
    markets = exch.load_markets()

    timeframe_model = {
        "dates": [],
        "open prices": [],
        "highest prices": [],
        "lowest prices": [],
        "close prices": [],
        "volumes": [],
    }
    all_timeframes = ["1w", "1d", "4h", "1h", "15m", "5m"]

    symbol = {}

    for timeframe_unit in all_timeframes:
        symbol[timeframe_unit] = copy.deepcopy(dict(timeframe_model))

    exchange = {}
    new_exchange = {}

    folder_name = "data_Folder"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # init dictionnary or take precedent state
    if symbol_name in markets:
        exchange[symbol_name] = copy.deepcopy(dict(symbol))
        file_name = (
            folder_name
            + "/"
            + exchange_name
            + "_"
            + symbol_name.split("/")[0]
            + "-"
            + symbol_name.split("/")[1]
            + "_data_History_Price_Action.json"
        )

        if os.path.isfile(file_name):
            exchange[symbol_name] = read_json_file(file_name)

    new_exchange = copy.deepcopy(exchange)

    if symbol_name in markets:
        new_exchange[symbol_name] = from_exc_to_raw_data_structure(
            exch,
            symbol_name,
            exchange,
            timeframe,
            all_timeframes,
            start_date,
        )

        file_name = (
            folder_name
            + "/"
            + exchange_name
            + "_"
            + symbol_name.split("/")[0]
            + "-"
            + symbol_name.split("/")[1]
            + "_data_History_Price_Action.json"
        )

        save_json_file(copy.deepcopy(new_exchange[symbol_name]), file_name)

    return file_name
