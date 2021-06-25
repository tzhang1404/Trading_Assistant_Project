import pandas as pd
import logging 
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError
from typing import List

from ..Constants.constants import IEXFINANCE_TOKEN
from .IEX_Stock_Data import IEX_RT_Price, IEX_RT_Price_Collection

class IEX_Stock_Query:
    
    def __init__(self, format: str="pandas"):
        self.format = "pandas"
    

    def query_realtime_price(self, ticker: str) -> IEX_RT_Price:
        '''
        DF Example
        <class 'pandas.core.frame.DataFrame'>
                 AAPL
        price  134.16
        '''
        try:
            stock = Stock(ticker, token=IEXFINANCE_TOKEN, output_format=self.format)    
            res_df = stock.get_price()
        except IEXQueryError as e:
            logging.log(str(e))
            return None
            
        return IEX_RT_Price(ticker=ticker, price=res_df.iloc[0,0], date=pd.Timestamp.now())
    

    def query_multiple_realtime_prices(self, tickers: List[str]) -> IEX_RT_Price_Collection:

        data_collection = IEX_RT_Price_Collection()
        for ticker in tickers:
            rt_stock_data = self.query_realtime_price(ticker=ticker)
            data_collection.add_stock_data(rt_stock_data)
        return data_collection

    
    