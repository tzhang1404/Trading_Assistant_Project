import pandas as pd

from typing import List
from .Portfolio_Stock import Portfolio_Stock
from .Portfolio_Data_Reader import Data_Reader
from ..Constants.constants import PORTFOLIO_HEADERS

class Portfolio_Stock_Collection: 

    @staticmethod
    def sanity_check_portfolio_df(df: pd.DataFrame) -> bool:
        if df is None:
            return False
        df_headers = df.columns
        for header in PORTFOLIO_HEADERS:
            if header not in df_headers:
                return False
        return True

    @classmethod
    def from_reading_data(Portfolio_Stock_Collection, path: str="", is_csv: bool=False):
        df = None
        if is_csv:
            df = Data_Reader.read_csv(path=path)
        else:
            df = Data_Reader.read_excel(path=path)
        return Portfolio_Stock_Collection(df=df)        

    def __init__(self, df: pd.DataFrame):
        if not Portfolio_Stock_Collection.sanity_check_portfolio_df(df):
            raise ValueError(f"Dataframe column names does not fit")
        self.portfolio_stocks = {}
        for i in range(df.shape[0]):
            df_row = df.iloc[i]
            ticker = df_row["ticker"]
            self.portfolio_stocks[ticker] = Portfolio_Stock.from_pd_series(series=df_row)
    
    def get_stock(self, ticker: str) -> Portfolio_Stock:
        return self.portfolio_stocks[ticker]
    
    def get_all_tickers(self) -> List[str]:
        return [*self.portfolio_stocks.keys()]
    
    def get_all_data_list(self) -> List[Portfolio_Stock]:
        return [*self.portfolio_stocks.values()]
    