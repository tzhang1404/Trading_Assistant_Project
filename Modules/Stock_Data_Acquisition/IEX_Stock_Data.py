import pandas as pd
from typing import List

class IEX_Stock_Data:

    def __init__(self, ticker: str):
        self.ticker = ticker
    

class IEX_RT_Price(IEX_Stock_Data):
    
    def __init__(self, ticker: str, price: float, date: pd.Timestamp):
        super().__init__(ticker)
        self.price = price
        self.date = date
    
    

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class IEX_RT_Price_Collection:

    def __init__(self):
        self.data_dict = {}

    def add_stock_data(self, rt_price_data: IEX_RT_Price) -> None:
        self.data_dict[rt_price_data.ticker] = rt_price_data
    
    def get_all_tickers(self) -> List[str]:
        return [*self.data_dict.keys()]
    
    def get_stock_data(self, ticker: str) -> IEX_RT_Price:
        if ticker in self.data_dict:
            return self.data_dict[ticker]
        else:
            return None

    def get_all_data_list(self) -> List[IEX_RT_Price]:
        return [*self.data_dict.values()]
    
    def debug_print_all_price(self) -> None:
        for key, value in self.data_dict.items():
            print(key, value.price)
            
    
                
        
        