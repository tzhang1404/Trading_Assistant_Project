import pandas as pd
import logging

from typing import Dict, List

from ..Constants.constants import Interval

class Price_Data:
    def __init__(self, dataframe: pd.DataFrame, ticker: str):
        self.dataframe = dataframe
        self.ticker = ticker

class Daily_Data(Price_Data):
    def __init__(self, dataframe: pd.DataFrame, ticker: str):
        super().__init__(dataframe, ticker)

class Intraday_Data(Price_Data):
    def __init__(self, dataframe: pd.DataFrame, ticker: str, interval: Interval):
        super().__init__(dataframe, ticker)
        self.interval = interval

class Stock_Data:
    '''
    Class for storing the price data and metadata for one stock 
    '''
    def __init__(self, dataframe: pd.DataFrame, ticker: str, interval: Interval=None, is_intraday: bool=False):
        if is_intraday:
            if interval is None:
                raise TypeError("Expected Valid Interval")
            self.data = Intraday_Data(dataframe=dataframe, ticker=ticker, interval=interval)
        else:
            self.data = Daily_Data(dataframe=dataframe, ticker=ticker)
    
    def get_dataframe(self):
        return self.data.dataframe

    def get_ticker(self):
        return self.data.ticker


class Stock_Data_Storage:
    
    def __init__(self):
        self.Data_Dictionary = {}
        self.tickers = []
    
    def add_data(self, stock_data: Stock_Data) -> None:
        '''
        Store the inputed data into the Data_Dictionary
        '''
        ticker = stock_data.get_ticker()
        if ticker in self.Data_Dictionary:
            logging.warning(f"Adding duplicated stock data for {ticker}")
        self.Data_Dictionary[ticker] = stock_data
        self.tickers.append(ticker)
    
    def get_data(self, ticker: str) -> Stock_Data:
        '''
        Returns the appropreiate stock_data in the dictionary
        '''
        if not ticker in self.Data_Dictionary:
            raise ValueError(f"Looking for a non-existent ticker {ticker}")
        else:
            return self.Data_Dictionary[ticker]

    def get_tickers(self) -> List[str]:
        return self.tickers

    
