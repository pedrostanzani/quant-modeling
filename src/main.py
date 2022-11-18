import pandas as pd
from datetime import date


def how_many_days_since_last_trading_day(today_date, df):
    """
    :param date today_date:
    :param pd.DataFrame df: DataFrame with a datetime index
    """
    quotes_until_now = df.loc[:today_date, :].reset_index(names='index')
    
    last_day = quotes_until_now.iloc[-1]['index']
    if last_day.date() == today_date:
        last_day = quotes_until_now.iloc[-2]['index']
    
    return today_date - last_day.date()


def trading_day_immediately_before(today_date, df):        
    return today_date - how_many_days_since_last_trading_day(today_date, df)


def get_tickers(*args):
    """
    get_tickers() is meant to be implemented by the strategy
    developer. Ideally, it receives a rebalancing date as a 
    parameter and returns a list of tickers that will be
    purchased on that date.

    Here, get_tickers() is a just dummy function.
    """
    return ['PETR4', 'VALE3', 'ITUB4']


def run_backtest(
    close: pd.DataFrame, 
    start_date: date, 
    end_date: date, 
    rebalance: int,
    get_tickers: function
    ):
    """
    :param pd.DataFrame close: DataFrame of closing prices with a datetime index
    :param date start_date:
    :param date end_date:
    :param date rebalance: rebalancing time delta in months
    """
    portfolio = pd.DataFrame()
    
    today = pd.Timestamp(start_date)
    while today.date() <= end_date:
        next_date = today + pd.DateOffset(months=rebalance)
        
        # Asset selection
        tickers = get_tickers(close, today)
        
        # Once we have our tickers, we assemble our quotes
        first_quote = trading_day_immediately_before(today.date(), close)
        last_quote  = trading_day_immediately_before(next_date.date(), close)
        
        iteration_returns = close.loc[first_quote:last_quote, tickers].pct_change().mean(axis=1)
        iteration_returns = iteration_returns.to_frame(name='pctChange')
        iteration_returns = iteration_returns.iloc[1:].loc[:end_date]
        
        portfolio = pd.concat([portfolio, iteration_returns])
        
        today = next_date
        
    return portfolio
