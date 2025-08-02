import pandas as pd
from typing import List, Tuple


def compute_win_loss_ratio(
    win_trades: int,
    total_profit: float,
    loss_trades: int,
    total_loss: float,
    profit: float,
):
    """compute all the metrics for a global win/loss ratio

    Args:
        win_trades (int): _description_
        total_profit (float): _description_
        loss_trades (int): _description_
        total_loss (float): _description_
        profit (float): _description_

    Returns:
        _type_: _description_
    """
    if profit > 0:
        win_trades += 1
        total_profit += profit
    elif profit <= 0:
        loss_trades += 1
        total_loss += profit

    return win_trades, total_profit, loss_trades, total_loss


def compute_long_win_loss_ratio(
    win_trades_long: int,
    total_profit_long: float,
    loss_trades_long: int,
    total_loss_long: float,
    profit: float,
):
    """compute all the metrics for a long win/loss ratio

    Args:
        win_trades_long (int): _description_
        total_profit_long (float): _description_
        loss_trades_long (int): _description_
        total_loss_long (float): _description_
        profit (float): _description_

    Returns:
        _type_: _description_
    """

    if profit > 0:
        win_trades_long += 1
        total_profit_long += profit
    elif profit <= 0:
        loss_trades_long += 1
        total_loss_long += profit

    return win_trades_long, total_profit_long, loss_trades_long, total_loss_long


def compute_short_win_loss_ratio(
    win_trades_short: int,
    total_profit_short: float,
    loss_trades_short: int,
    total_loss_short: int,
    profit: float,
):
    """compute all the metrics for a short win/loss ratio

    Args:
        win_trades_short (int): _description_
        total_profit_short (float): _description_
        loss_trades_short (int): _description_
        total_loss_short (int): _description_
        profit (float): _description_

    Returns:
        _type_: _description_
    """
    if profit > 0:
        win_trades_short += 1
        total_profit_short += profit
    elif profit <= 0:
        loss_trades_short += 1
        total_loss_short += profit

    return win_trades_short, total_profit_short, loss_trades_short, total_loss_short


def compute_year_results(
    trade_index: int,
    current_trade: pd.DataFrame,
    profits_month_one_year: float,
    profits_month: float,
    profits_year: float,
    years_trade_position_timeframe: List[Tuple[pd.DataFrame, int]],
    previous_trade: pd.DataFrame,
    wallet: float,
):
    """this function computes the detailed results for one year on a month scale

    Args:
        trade_index (int): _description_
        current_trade (pd.DataFrame): _description_
        profits_month_one_year (float): _description_
        profits_month (float): _description_
        profits_year (float): _description_
        years_trade_position_timeframe (List[Tuple[pd.DataFrame, int]]): _description_
        previous_trade (pd.DataFrame): _description_
        wallet (float): _description_

    Returns:
        _type_: _description_
    """

    current_month = str(current_trade["month"].item())
    current_year = str(current_trade["year"].item())
    current_wallet = current_trade["year"].item()

    current_wallet = current_trade["usdt size wallet"].item()
    if current_month != previous_trade["Month"]:
        if current_year != previous_trade["Year"]:
            # for order book history and display
            year_trade_position = (current_trade["year"].item(), trade_index)
            years_trade_position_timeframe.append(year_trade_position)

            if previous_trade["Year"] != "":
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
                year = current_trade["year"].item()
                profits_year[year] = (
                    (current_wallet - wallet["precedentYear"])
                    / wallet["precedentYear"]
                    * 100
                )
                profits_month[year] = profits_month_one_year
            previous_trade["Year"] = current_year
            wallet["precedentYear"] = current_wallet

        if previous_trade["Month"] != "":
            month = current_trade["month"].item()
            year = current_trade["year"].item()
            profits_month_one_year[month] = (
                (current_wallet - wallet["precedentMonth"])
                / wallet["precedentMonth"]
                * 100
            )
        previous_trade["Month"] = current_month
        wallet["precedentMonth"] = current_wallet

    return (
        years_trade_position_timeframe,
        profits_year,
        profits_month_one_year,
        profits_month,
        previous_trade,
        wallet,
    )
