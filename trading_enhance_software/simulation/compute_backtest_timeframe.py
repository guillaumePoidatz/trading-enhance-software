import pandas as pd
from simulation.compute_one_trade import compute_one_trade
from utils.simulation_utils import compute_win_loss_ratio
from utils.simulation_utils import compute_long_win_loss_ratio
from utils.simulation_utils import compute_short_win_loss_ratio
from utils.simulation_utils import compute_year_results


def compute_backtest_timeframe(
    strat, df_backtest_timeframe: pd.DataFrame, usdt: float, coin: float, fees: float
):
    """compute the backtest for one timeframe

    Args:
        strat (_type_): _description_
        df_backtest_timeframe (pd.DataFrame): _description_
        usdt (float): _description_
        coin (float): _description_
        fees (float): _description_

    Returns:
        _type_: return all the trade data of one timeframe
    """
    backtest_datas = dict()
    strat.set_indicators()
    trade_characteristics = [
        "date",
        "position",
        "order",
        "close price",
        "fees",
        "usdt size wallet",
        "year",
        "month",
    ]
    df_trades_timeframe = pd.DataFrame(
        columns=trade_characteristics
    )  # order book history for a time frame
    years_timeframe = []
    fees = 1 - fees / 100
    strat.usdt = usdt
    strat.coin = coin

    # useful to compute drawback
    last_ath = 0
    win_trades = 0
    loss_trades = 0
    total_loss = 0
    total_profit = 0
    win_trades_long = 0
    total_profit_long = 0
    loss_trades_long = 0
    total_loss_long = 0
    win_trades_short = 0
    total_profit_short = 0
    loss_trades_short = 0
    total_loss_short = 0
    max_drawback = 0
    number_of_trades = 0
    number_of_longs = 0
    number_of_shorts = 0
    profits_year_timeframe = {}
    profits_month_timeframe = {}
    profits_month_one_year = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
    }
    start_year = df_backtest_timeframe.loc[0, "dates"].year
    end_year = df_backtest_timeframe.loc[
        len(df_backtest_timeframe["dates"]) - 1, "dates"
    ].year
    for i in range(start_year, end_year + 1):
        profits_month_timeframe[i] = profits_month_one_year
        profits_year_timeframe[i] = 0

    # useful for compute_year_results
    wallet = {"precedentMonth": 0}
    precedent = {"Month": "", "Year": ""}

    for index, price in enumerate(df_backtest_timeframe["close prices"]):
        strat.set_short_long()

        # compute the possibility of a liquidation
        if strat.enter_price_long is not None and strat.enter_price_long != 0:
            long_current_ratio = (
                (price * fees - strat.enter_price_long)
                / strat.enter_price_long
                * strat.leverage
            )
        else:
            long_current_ratio = 0
        if strat.enter_price_short is not None and strat.enter_price_short != 0:
            short_current_ratio = (
                (strat.enter_price_short - price * fees)
                / strat.enter_price_short
                * strat.leverage
            )
        else:
            short_current_ratio = 0

        # the liquidation case
        if long_current_ratio + short_current_ratio <= -1:
            compute_one_trade(
                strat,
                price,
                df_backtest_timeframe,
                "-",
                index,
                trade_characteristics,
                df_trades_timeframe,
                fees,
            )

        # if possible compute one trade
        if strat.long_condition is True:
            trade_to_add, df_trades_timeframe = compute_one_trade(
                strat,
                price,
                df_backtest_timeframe,
                "long",
                index,
                trade_characteristics,
                df_trades_timeframe,
                fees,
            )

        elif strat.short_condition is True:
            trade_to_add, df_trades_timeframe = compute_one_trade(
                strat,
                price,
                df_backtest_timeframe,
                "short",
                index,
                trade_characteristics,
                df_trades_timeframe,
                fees,
            )

        elif strat.close_long_condition is True:
            trade_to_add, df_trades_timeframe = compute_one_trade(
                strat,
                price,
                df_backtest_timeframe,
                "close long",
                index,
                trade_characteristics,
                df_trades_timeframe,
                fees,
            )

            profit = (
                (strat.close_price_long - strat.enter_price_long)
                / strat.enter_price_long
                * 100
            )
            win_trades, total_profit, loss_trades, total_loss = compute_win_loss_ratio(
                win_trades, total_profit, loss_trades, total_loss, profit
            )
            win_trades_long, total_profit_long, loss_trades_long, total_loss_long = (
                compute_long_win_loss_ratio(
                    win_trades_long,
                    total_profit_long,
                    loss_trades_long,
                    total_loss_long,
                    profit,
                )
            )
            number_of_longs += 1
            number_of_trades += 1

        elif strat.close_short_condition is True:
            trade_to_add, df_trades_timeframe = compute_one_trade(
                strat,
                price,
                df_backtest_timeframe,
                "close short",
                index,
                trade_characteristics,
                df_trades_timeframe,
                fees,
            )
            profit = (
                (strat.close_price_short - strat.enter_price_short)
                / strat.enter_price_short
                * 100
            )
            win_trades, total_profit, loss_trades, total_loss = compute_win_loss_ratio(
                win_trades, total_profit, loss_trades, total_loss, profit
            )
            (
                win_trades_short,
                total_profit_short,
                loss_trades_short,
                total_loss_short,
            ) = compute_short_win_loss_ratio(
                win_trades_short,
                total_profit_short,
                loss_trades_short,
                total_loss_short,
                profit,
            )
            number_of_shorts += 1
            number_of_trades += 1

        if (
            strat.long_condition is True
            or strat.short_condition is True
            or strat.close_long_condition is True
            or strat.close_short_condition is True
        ):
            # results for each  year
            (
                years_timeframe,
                profits_year_timeframe,
                profits_month_one_year,
                profits_month_timeframe,
                precedent,
                wallet,
            ) = compute_year_results(
                number_of_trades,
                trade_to_add,
                profits_month_one_year,
                profits_month_timeframe,
                profits_year_timeframe,
                years_timeframe,
                precedent,
                wallet,
            )

        strat.k_point += 1
        # compute ATH (all time highest)
        last_ath = max(last_ath, strat.usdt + strat.coin * price)
        if (strat.usdt + strat.coin * price) != last_ath:
            max_drawback = min(
                max_drawback,
                (strat.usdt + strat.coin * price - last_ath) / last_ath * 100,
            )

    backtest_datas = {
        "total profit": total_profit,
        "total loss": total_loss,
        "win trades": win_trades,
        "loss trades": loss_trades,
        "total profit long": total_profit_long,
        "total loss long": total_loss_long,
        "win trades long": win_trades_long,
        "loss trades long": loss_trades_long,
        "total profit short": total_profit_short,
        "total loss short": total_loss_short,
        "win trades short": win_trades_short,
        "loss trades short": loss_trades_short,
        "usdt": strat.usdt,
        "coin": strat.coin,
        "number of trade": number_of_trades,
        "number of long": number_of_longs,
        "number of short": number_of_shorts,
        "last price": price,
        "max drawback": max_drawback,
        "order book history timeframe": df_trades_timeframe,
        "order book per year timeframe": years_timeframe,
        "profits per month timeframe": profits_month_timeframe,
        "profits per year timeframe": profits_year_timeframe,
    }
    return backtest_datas
