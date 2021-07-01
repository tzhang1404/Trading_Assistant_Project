from typing import List

from ..Portfolio_Acquisition.Portfolio_Stock_Collection import Portfolio_Stock_Collection
from ..Portfolio_Acquisition.Portfolio_Stock import Portfolio_Stock
from ..Stock_Data_Acquisition.IEX_Stock_Data import IEX_RT_Price, IEX_RT_Price_Collection
from .Price_Delta import Price_Delta
from .Stock_Performance_Result import Stock_Performance_Result

class Stock_Performance():
    
    def __init__(self, port_stock: Portfolio_Stock):
        self.portfolio_data = port_stock
        self.price_delta = Price_Delta()
        self.indicator_results = None
        self.performance_result = Stock_Performance_Result()
        self.rt_price_data = None

    
    def get_ticker(self) -> str:
        return self.portfolio_data.ticker
    
    def get_action_result(self):
        return self.performance_result.stock_action
    

    def analyze_realtime_price(self, rt_price_data: IEX_RT_Price):
        self.rt_price_data = rt_price_data
        self.price_delta.using_rt_price(rt_price=rt_price_data.price, comparing_to=self.portfolio_data.purchase_price)
        if self.price_delta.rt_price_delta < -(self.portfolio_data.decrease_limit):
            self.performance_result.attach_loss_sell_action(actual_delta=self.price_delta.rt_price_delta)
        
        if self.price_delta.rt_price_delta > self.portfolio_data.increase_limit:
            self.performance_result.attach_profit_sell_action(actual_delta=self.price_delta.rt_price_delta)
    

    def debug_print_performance_result(self):
        print(f"{self.portfolio_data.ticker}'s action result is {self.performance_result.stock_action}")
        print(f"The purchase price of {self.portfolio_data.ticker} was {self.portfolio_data.purchase_price} and current price is {self.rt_price_data.price}")


class Stock_Performance_Collection():
    
    def __init__(self):
        self.data = {}

    def consume_stock_performance(self, sp: Stock_Performance):
        self.data[sp.get_ticker()] = sp

    @classmethod
    def analyze_all_realtime_price(
        Stock_Performance_Collection, 
        port_collection: Portfolio_Stock_Collection, 
        price_collection: IEX_RT_Price_Collection):

        sp_collection = Stock_Performance_Collection()

        portfolio_stock_list = port_collection.get_all_data_list()
        rt_price_data_list = price_collection.get_all_data_list()

        if len(portfolio_stock_list) != len(rt_price_data_list):
            raise ValueError("Portfolio List and RT price list does not equal in length")
        
        for i in range(0, len(portfolio_stock_list)):
            port_stock = portfolio_stock_list[i]
            rt_price = rt_price_data_list[i]
            stock_performance = Stock_Performance(port_stock=port_stock)
            stock_performance.analyze_realtime_price(rt_price_data=rt_price)
            sp_collection.consume_stock_performance(sp=stock_performance)
        
        return sp_collection
    
    
    def get_all_stock_performances(self) -> List[Stock_Performance]:
        return [*self.data.values()]


    def get_stock_action_count(self) -> int:
        sp_list = self.get_all_stock_performances()
        count = 0
        for sp in sp_list:
            if sp.performance_result.stock_action is not None:
                count += 1
        return count
    

    def debug_print_all_performance_result(self):
        for _ticker, performance in self.data.items():
            performance.debug_print_performance_result()
        


        
        
    
        
        
        
        
        
        
    
        
        