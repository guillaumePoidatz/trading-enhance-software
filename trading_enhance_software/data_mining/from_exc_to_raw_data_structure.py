# manage all types of data to feed the backtest
import time
from datetime import datetime, timedelta


def from_exc_to_raw_data_structure(
    exchange, symbol, raw_data, timeframe, all_timeframes, start_date
):
    """This function is transforming raw data from exchanges to a formatted dictionary

    Args:
        exchange (_type_): _description_
        symbol (_type_): _description_
        raw_data (_type_): _description_
        timeframe (_type_): _description_
        all_timeframes (_type_): _description_
        start_date (_type_): _description_

    Returns:
        _type_: the formatted dictionary containing the data with this structure:

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

    data = {}
    data[symbol] = {}

    data = raw_data

    allTfOutOfTf = [
        tfElement for tfElement in all_timeframes if tfElement not in timeframe
    ]

    timeframe_in_ms = {
        "1w": 7 * 24 * 3600 * 1000,
        "1d": 24 * 3600 * 1000,
        "4h": 4 * 3600 * 1000,
        "1h": 3600 * 1000,
        "15m": 15 * 60 * 1000,
        "5m": 5 * 60 * 1000,
    }

    # compute the limit history in one request
    ohlcv = exchange.fetch_ohlcv("BTC/USDT", "1w")
    wlimit = len(ohlcv) - 1
    historyLimit = {
        "1w": wlimit,
        "1d": wlimit * 7,
        "4h": wlimit * 7 * 6,
        "1h": wlimit * 7 * 24,
        "15m": wlimit * 7 * 24 * 4,
        "5m": wlimit * 7 * 24 * 12,
    }

    # compute the start date which depending on the user command but also of the exchange history
    endDate = time.time() * 1000

    currentDate = datetime.now()
    targetDate = currentDate - timedelta(weeks=wlimit)
    start_date = max(start_date, int(targetDate.timestamp()) * 1000)

    for tfElement in timeframe:
        # manage last date of the current dictionnary to reduce the time to colect datas
        if len(raw_data[symbol][tfElement]["dates"]) == 0:
            lastDate = start_date
        else:
            lastDate = raw_data[symbol][tfElement]["dates"][-1]

        # loop to have all the datas (history limit in one request)
        while lastDate < endDate - timeframe_in_ms[tfElement]:
            ohlcv = exchange.fetch_ohlcv(
                symbol, tfElement, since=lastDate, limit=historyLimit[tfElement]
            )
            # maybe we need this line to not saturate the exchange
            # time.sleep(60/rateLimit)
            dates = []
            open_prices = []
            highest_prices = []
            lowest_prices = []
            close_prices = []
            volumes = []

            # put datas in our dictionnary, 2 possibilities : either no precedent datas or precedent datas
            if (
                len(raw_data[symbol][tfElement]["dates"]) == 0
                or raw_data[symbol][tfElement]["dates"] == -1
            ):
                for entry in ohlcv:
                    dates.append(entry[0])
                    open_prices.append(entry[1])
                    highest_prices.append(entry[2])
                    lowest_prices.append(entry[3])
                    close_prices.append(entry[4])
                    volumes.append(entry[5])

                data[symbol][tfElement]["dates"] = dates
                data[symbol][tfElement]["open prices"] = open_prices
                data[symbol][tfElement]["highest prices"] = highest_prices
                data[symbol][tfElement]["lowest prices"] = lowest_prices
                data[symbol][tfElement]["close prices"] = close_prices
                data[symbol][tfElement]["volumes"] = volumes

            else:
                for i in range(len(ohlcv)):
                    idx = len(ohlcv)
                    if ohlcv[i][0] == raw_data[symbol][tfElement]["dates"][-1]:
                        idx = i
                        break

                if idx < len(ohlcv) - 1:
                    index_range = list(range(idx + 1, len(ohlcv)))

                    for i in index_range:
                        dates.append(ohlcv[i][0])
                        open_prices.append(ohlcv[i][1])
                        highest_prices.append(ohlcv[i][2])
                        lowest_prices.append(ohlcv[i][3])
                        close_prices.append(ohlcv[i][4])
                        volumes.append(ohlcv[i][5])

                    data[symbol][tfElement]["dates"] = (
                        raw_data[symbol][tfElement]["dates"] + dates
                    )
                    data[symbol][tfElement]["open prices"] = (
                        raw_data[symbol][tfElement]["open prices"] + open_prices
                    )
                    data[symbol][tfElement]["highest prices"] = (
                        raw_data[symbol][tfElement]["highest prices"] + highest_prices
                    )
                    data[symbol][tfElement]["lowest prices"] = (
                        raw_data[symbol][tfElement]["lowest prices"] + lowest_prices
                    )
                    data[symbol][tfElement]["close prices"] = (
                        raw_data[symbol][tfElement]["close prices"] + close_prices
                    )
                    data[symbol][tfElement]["volumes"] = (
                        raw_data[symbol][tfElement]["volumes"] + volumes
                    )
            lastDate = data[symbol][tfElement]["dates"][-1]

        # now we're stocking all the datas of the other timeframe to not erase our datas in the process of rewritting the dat file
        for tfElement in allTfOutOfTf:
            data[symbol][tfElement]["dates"] = raw_data[symbol][tfElement]["dates"]
            data[symbol][tfElement]["open prices"] = raw_data[symbol][tfElement][
                "open prices"
            ]
            data[symbol][tfElement]["highest prices"] = raw_data[symbol][tfElement][
                "highest prices"
            ]
            data[symbol][tfElement]["lowest prices"] = raw_data[symbol][tfElement][
                "lowest prices"
            ]
            data[symbol][tfElement]["close prices"] = raw_data[symbol][tfElement][
                "close prices"
            ]
            data[symbol][tfElement]["volumes"] = raw_data[symbol][tfElement]["volumes"]

    return data[symbol]
