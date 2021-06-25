import logging
import pandas as pd
import time

from alpha_vantage.timeseries import TimeSeries
from typing import Dict, List

from ..Constants.constants import (
    ALPHAVANTAGE_KEY, 
    FREQUENCY_EXCEPTION_KEY_WORD, 
    Interval)
from .Stock_Data import Stock_Data, Stock_Data_Storage

class QueryFrequencyException(Exception):
    '''
    Exception Class raised when encountered a API frequency warning
    '''
    pass


class Stock_Query:

    key = ALPHAVANTAGE_KEY

    def __init__(self, output_format = "pandas"):
        self.query = TimeSeries(key=self.key, output_format=output_format)
        self.tickers = []
    

    def get_stocks_data(self, tickers: List, Interval: Interval=None) -> Stock_Data_Storage:
        '''
        Get multiple stock data based on the input list, since AlphaVantage's free API
        only supports FIVE queries per minute and 500 queries in total a day, we need to throttle our queries
        '''
        self.check_tickers_input(tickers)
        self.tickers = tickers

        print(f"Querying for {len(tickers)} stocks, estimiated runtime: {self.estimate_run_time(tickers)} minute(s)")

        stock_data_storage = Stock_Data_Storage()
        while self.has_stocks():
            ticker = self.get_next_stock()
            try:
                stock_data = self.query_one_stock(ticker=ticker, Interval=Interval)
                stock_data_storage.add_data(stock_data=stock_data)
            except QueryFrequencyException:
                print(f"Frequency Warning detected when querying {ticker}, force cool-down...")
                self.cool_down(elapsed_secs=0)
                # retry this query with extra cooldown
                self.restore_stock(ticker=ticker)
            except Exception as error:
                logging.error(f"Error when quering {ticker}: {str(error)}")
                raise error

        return stock_data_storage

    
    def query_one_stock(self, ticker, Interval: Interval) -> Stock_Data:
        '''
        Process one stock at a time
        '''
        if Interval:
            result = self._get_intraday_price_data(ticker = ticker, interval=Interval)
        else:
            result = self._get_daily_price_data(ticker = ticker)
        return result


    def get_next_stock(self) -> str:
        '''
        Collect the next five stocks to process in a minute
        '''
        if not self.has_stocks():
            return None
        else:
            ticker = self.tickers[0]
            self.tickers = self.tickers[1:]
            return ticker
    
    def restore_stock(self, ticker: str) -> None:
        """
        Put ticker back in case of a frequency error
        so that the ticker can be queried again
        """
        self.tickers.insert(0, ticker)

    
    def has_stocks(self) -> bool:
        if self.tickers and len(self.tickers) > 0:
            return True
        else:
            return False
    

    def check_tickers_input(self, tickers: List[str]) -> None:
        if tickers is None or type(tickers) != list:
            raise TypeError("Invalid Ticker List Input")
        elif len(tickers) == 0:
            raise ValueError("No Tickers Input")
        else:
            return
        

    def _get_daily_price_data(self, ticker: str, full_history: bool=False) -> Stock_Data:
        '''
        Queries daily price OHLC data for the given ticker
        Set full_history to true to query all available data, else most recent 100 rows will be returned
        '''
        try:
            data = self.query.get_daily(symbol=ticker, outputsize= 'full' if full_history else 'compact')[0]
        except Exception as error:
            if Stock_Query.is_freqency_exception(error):
                raise QueryFrequencyException()
            raise error

        data = self.reset_column_names(data=data)

        return Stock_Data(dataframe=data, ticker=ticker)
    
    def _get_intraday_price_data(self, ticker: str, interval: Interval, full_history: bool=False) -> Stock_Data:
        '''
        Queries intra-day price OHLC data for the given ticker with the given interval
        Interval has 1, 5, 30, 60 mins
        '''
        try:
            data = self.query.get_intraday(symbol=ticker, interval=interval.value, outputsize= 'full' if full_history else 'compact')[0]
        except Exception as error:
            if Stock_Query.is_freqency_exception(error):
                raise QueryFrequencyException()
            raise error
            
        data = self.reset_column_names(data=data)

        return Stock_Data(dataframe=data, ticker=ticker, interval=interval, is_intraday=True)

    
    def reset_column_names(self, data: pd.DataFrame) -> pd.DataFrame:
        '''
        Reset the column names into more readable forms
        '''
        data.columns = ["open", "high", "low", "close", "volume"]
        return data
    
    def cool_down(self, elapsed_secs: int) -> None:
        '''
        Sleep for the appropriate seconds to prevent API errors 
        from querying too much in a minute 
        '''
        if elapsed_secs >= 60:
            return
        print("Waiting for API Cool-Down...")
        sleep_time = 60 - elapsed_secs
        time.sleep(sleep_time)


    def estimate_run_time(self, tickers: List) -> int:
        return int(len(tickers) / 5)

    
    @staticmethod
    def is_freqency_exception(e: Exception) -> bool:
        '''
        Analyze the error message from the API to determine if it is a frequency warning
        '''
        return FREQUENCY_EXCEPTION_KEY_WORD in str(e)

