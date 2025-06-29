import pandas as pd
from trading_enhance_software.simulation.compute_backtest_timeframe import (
    compute_backtest_timeframe,
)


def analyze_backtest_datas(
    timeframe_unit: str,
    df_backtest: pd.DataFrame,
    general_informations: pd.DataFrame,
    df_trades: dict,
    years: dict,
    initial_usdt: float,
    initial_coin: float,
    profits_month: float,
    profits_year: float,
    strat_name: str,
    fees: float,
):
    """this function is analyzing all the trade data on one timeframe and computing assessment
    metrics about the efficiency of the trading strategy

    Args:
        timeframe_unit (str): _description_
        df_backtest (pd.DataFrame): _description_
        general_informations (pd.DataFrame): _description_
        df_trades (dict): _description_
        years (dict): _description_
        initial_usdt (float): _description_
        initial_coin (float): _description_
        profits_month (float): _description_
        profits_year (float): _description_
        strat_name (str): _description_
        fees (float): _description_
    """
    strat_module = __import__(f"strategies.{strat_name}", fromlist=[strat_name])
    strat_class = getattr(strat_module, strat_name)
    strat = strat_class(df=df_backtest[timeframe_unit], usdt=initial_usdt, coin=0)

    df_backtest_timeframe = df_backtest[timeframe_unit]

    # buy and hold performance
    performance_buy_and_hold = (
        initial_usdt
        / df_backtest_timeframe.loc[0, "close prices"]
        * df_backtest_timeframe.loc[len(df_backtest_timeframe) - 1, "close prices"]
    )

    # backtest for one timeframe
    backtest_datas = compute_backtest_timeframe(
        strat, df_backtest[timeframe_unit], initial_usdt, initial_coin, fees
    )

    # all operations necessary for general informations
    if backtest_datas["win trades"] != 0:
        profit_average = backtest_datas["total profit"] / backtest_datas["win trades"]
    else:
        profit_average = backtest_datas["total profit"]

    if backtest_datas["loss trades"] != 0:
        loss_average = backtest_datas["total loss"] / backtest_datas["loss trades"]
    else:
        loss_average = backtest_datas["total loss"]

    if loss_average != 0:
        riskReward = profit_average / -loss_average
    else:
        riskReward = profit_average

    start_date = df_backtest_timeframe["dates"][0].strftime("%Y-%m-%d")
    end_date = df_backtest_timeframe["dates"][
        len(df_backtest_timeframe["dates"]) - 1
    ].strftime("%Y-%m-%d")
    period = start_date + "  " + end_date
    PnL = (
        (
            backtest_datas["usdt"]
            + backtest_datas["coin"] * backtest_datas["last price"]
            - initial_usdt
        )
        / initial_usdt
        * 100
    )

    if backtest_datas["number of trade"] != 0:
        win_loss_ratio = (
            backtest_datas["win trades"] / (backtest_datas["number of trade"]) * 100
        )
    else:
        win_loss_ratio = 0

    strat_vs_buy_and_hold = (
        (
            backtest_datas["usdt"]
            + backtest_datas["coin"] * backtest_datas["last price"]
            - performance_buy_and_hold
        )
        / performance_buy_and_hold
        * 100
    )

    if backtest_datas["number of long"] != 0:
        win_loss_ratio_long = (
            backtest_datas["win trades long"] / (backtest_datas["number of long"]) * 100
        )
    else:
        win_loss_ratio_long = 0

    if backtest_datas["number of short"] != 0:
        win_loss_ratio_short = (
            backtest_datas["win trades short"]
            / (backtest_datas["number of short"])
            * 100
        )
    else:
        win_loss_ratio_short = 0

    gI = {
        "period": period,
        "strategy": strat_name,
        "PnL": str(round(PnL, 2)) + " %",
        "Strat vs Buy and Hold": str(round(strat_vs_buy_and_hold, 2)) + " %",
        "Win/Loss ratio": str(round(win_loss_ratio, 2)) + " %",
        "Risk Reward": str(round(riskReward, 2)),
        "number of Trades": str(round(backtest_datas["number of trade"], 2)),
        "Max Drawback": str(round(backtest_datas["max drawback"], 2)) + " %",
        "Win/Loss ratio short": str(round(win_loss_ratio_short, 2)) + " %",
        "number of Short": str(round(backtest_datas["number of short"], 2)),
        "Win/Loss ratio long": str(round(win_loss_ratio_long, 2)) + " %",
        "number of long": str(round(backtest_datas["number of long"], 2)),
    }

    index = pd.Index([0])
    general_informations[timeframe_unit] = pd.DataFrame(gI, index=index)

    df_trades[timeframe_unit] = backtest_datas["order book history timeframe"]
    years[timeframe_unit] = backtest_datas["order book per year timeframe"]
    profits_month[timeframe_unit] = backtest_datas["profits per month timeframe"]
    profits_year[timeframe_unit] = backtest_datas["profits per year timeframe"]
