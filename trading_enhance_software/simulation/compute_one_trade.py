import pandas as pd


# here is the compute of the evolution of your wallet through one trade
def compute_one_trade(
    strat,
    price: float,
    df_backtest_timeframe: pd.DataFrame,
    type_of_trade: str,
    index: int,
    trade_characteristics,
    df_trades_timeframe: list[str],
    fees: float,
):
    """This function is responsible of simulating the action of one trade

    Args:
        strat (_type_): _description_
        price (float): _description_
        df_backtest_timeframe (pd.DataFrame): _description_
        type_of_trade (str): _description_
        index (int): _description_
        trade_characteristics (_type_): _description_
        df_trades_timeframe (list[str]): _description_
        fees (float): _description_

    Returns:
        _type_: the order book with the trade added
    """

    if type_of_trade == "-" and (strat.usdt != 0 or strat.coin != 0):
        strat.coin = 0
        strat.usdt = 0
        strat.is_short = False
        strat.is_long = False
    elif type_of_trade == "long":
        strat.enter_price_long = price
        strat.coin = strat.usdt * fees / strat.enter_price_long
        strat.usdt = strat.usdt - strat.usdt
    elif type_of_trade == "close long":
        strat.close_price_long = price
        gain = (
            strat.close_price_long * fees - strat.enter_price_long
        ) / strat.enter_price_long * strat.leverage + 1
        strat.usdt = strat.coin * gain * strat.enter_price_long
        strat.coin = strat.coin - strat.coin
    elif type_of_trade == "short":
        strat.enter_price_short = price
        strat.coin = strat.usdt * fees / strat.enter_price_short
        strat.usdt = strat.usdt - strat.usdt
    elif type_of_trade == "close short":
        strat.close_price_short = price
        gain = (
            strat.enter_price_short - strat.close_price_short * fees
        ) / strat.enter_price_short * strat.leverage + 1
        strat.usdt = strat.coin * gain * strat.enter_price_short
        strat.coin = strat.coin - strat.coin

    if type_of_trade != "-":
        trade_to_add = pd.DataFrame(
            [
                [
                    df_backtest_timeframe["dates"][index],
                    strat.usdt + strat.coin * price,
                    type_of_trade,
                    df_backtest_timeframe["close prices"][index],
                    str(round((1 - fees) * 100, 4)),
                    strat.usdt + strat.coin * price,
                    df_backtest_timeframe.loc[index, "dates"].year,
                    df_backtest_timeframe.loc[index, "dates"].month,
                ]
            ],
            columns=trade_characteristics,
        )
        df_trades_timeframe = df_trades_timeframe._append(
            trade_to_add, ignore_index=True
        )
        return trade_to_add, df_trades_timeframe
    else:
        return None
