from ..Stock_Data_Acquisition.IEX_Stock_Data import IEX_RT_Price
from ..Portfolio_Acquisition.Portfolio_Stock import Portfolio_Stock

class Price_Delta:
    def __init__(self):
        self.rt_price_delta = 0.0

    def using_rt_price(self, rt_price: float, comparing_to: float):
        rt_price_delta = (rt_price - comparing_to) / comparing_to
        self.rt_price_delta = rt_price_delta
        
        

        