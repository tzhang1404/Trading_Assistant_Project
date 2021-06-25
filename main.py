from typing import List

from Modules.Portfolio_Acquisition.Portfolio_Stock_Collection import Portfolio_Stock_Collection
from Modules.Stock_Data_Acquisition.IEX_Stock_Query import IEX_Stock_Query
from Modules.Stock_Data_Acquisition.IEX_Stock_Data import IEX_RT_Price_Collection



def read_stock_list_from_portfolio() -> List[str]:
    portfolio_data = Portfolio_Stock_Collection.from_reading_data()
    stock_list = portfolio_data.get_all_stocks()
    return stock_list


def query_stock_prices_from_list(stock_list) -> IEX_RT_Price_Collection:
    stock_queryer = IEX_Stock_Query()
    res = stock_queryer.query_multiple_realtime_prices(tickers=stock_list)
    return res

def main():
    stock_list = read_stock_list_from_portfolio()
    stock_price_collection = query_stock_prices_from_list(stock_list=stock_list)
    stock_price_collection.debug_print_all_price()

    
    

main()