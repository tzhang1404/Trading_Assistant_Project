import pandas as pd

class Portfolio_Stock:

    def __init__(
                self, 
                ticker:str, 
                purchase_date: pd.Timestamp, 
                purchase_price: float, 
                shares: int, 
                increase_limit: float, 
                decrease_limit: float):
        self.ticker = ticker
        self.purchase_date = purchase_date
        self.purchase_price = purchase_price
        self.shares = shares
        self.increase_limit = increase_limit
        self.decrease_limit = decrease_limit
        self.initial_capital = purchase_price * float(shares)
    

    @classmethod
    def from_pd_series(Portfolio_Stock, series):
        try:
            ps = Portfolio_Stock(series["ticker"], 
                                    series["purchase_date"], 
                                    series["purchase_price"], 
                                    series["shares"], 
                                    series["rules_increase_limit"], 
                                    series["rules_decrease_limit"])
        except KeyError as e:
            print("The input df does not have the right column names")
            print(e)
            return
        return ps
    
    @classmethod
    def from_pd_dataframe(Portfolio_Stock, df, row_index):
        series = df.iloc[row_index]
        return Portfolio_Stock.from_pd_series(series)

        