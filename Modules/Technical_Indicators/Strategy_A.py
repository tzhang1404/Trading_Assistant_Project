import pandas as pd
import logging

from ..Constants.constants import Indicator_Signal
from ..Stock_Data_Acquisition.AlphaV_Stock_Data import Stock_Data, Stock_Data_Storage

from .BollBand import BollBand
from .MACD import MACD
from .RSI import RSI
from .Indicator_Results import Stock_Result, Stock_Result_Storage


class Strategy_A():
    '''
    Strategy 1
    Using RSI, BBand, and MACD, 
    With BBand taking the highest weight, RSI taking middle weight, and MACD taking lowest
    '''

    def __init__(self, stock_data_storage: Stock_Data_Storage, days_back: int=None, ):
        self.stock_data_storage = None
        self.days_back = days_back
        self.stock_result_storage = Stock_Result_Storage()
        if len(stock_data_storage.get_tickers()) == 0:
            logging.warning("No Stock Data Imported")
            return
        # print(f"Importing Stock Data for {stock_data_storage.get_tickers()}")
        self.stock_data_storage = stock_data_storage
        
    
    def analyze_stocks(self, RSI: bool=True, BBAND: bool=True, MACD: bool=True):
        if self.stock_data_storage is None:
            return
        for ticker in self.stock_data_storage.get_tickers():
            stock_result = self._analyze_stock(ticker, RSI, BBAND, MACD)
            self.stock_result_storage.add_result(stock_result=stock_result)
    
    def _analyze_stock(self, ticker: str, RSI: bool, BBAND: bool, MACD: bool) -> Stock_Result:
        stock_data = self.stock_data_storage.get_data(ticker=ticker)
        stock_result = Stock_Result(ticker = ticker)
        if RSI:
            self.analyze_stock_RSI(stock_data=stock_data, stock_result=stock_result)
        if BBAND:
            self.analyze_stock_BBAND(stock_data=stock_data, stock_result=stock_result)
        if MACD:
            self.analyze_stock_MACD(stock_data=stock_data, stock_result=stock_result)
        
        return stock_result

    
    def get_result_storage(self):
        return self.stock_result_storage
    

    def analyze_stock_RSI(self, stock_data: Stock_Data, stock_result: Stock_Result, periods_back: int=5):
        rsi_df = RSI(stock_data=stock_data, days_back=self.days_back)
        latest_rsi = rsi_df['RSI'].iloc[0]

        sig_periods = self._rsi_count_significant_periods(df = rsi_df, periods_back=periods_back)

        if latest_rsi >= 70:
            stock_result.add_signal(indicator="RSI", signal=Indicator_Signal.Strong_Bearish)
        elif latest_rsi <= 30:
            stock_result.add_signal(indicator="RSI", signal=Indicator_Signal.Strong_Bullish)
        
        return stock_result
    
    def _rsi_count_significant_periods(self, df: pd.DataFrame, periods_back: int) -> int:
        '''
        Deprecated strategy desigin
        '''
        if periods_back > df.shape[0]:
            raise ValueError("Periods back larger than dataframe length")
        period_back_df = df.iloc[:periods_back]
        count_df = period_back_df[(period_back_df['RSI'] >= 70) | (period_back_df['RSI'] <= 30)].count()
        return count_df['RSI']
    

    def analyze_stock_BBAND(self, stock_data: Stock_Data, stock_result: Stock_Result):
        price_df = stock_data.get_dataframe()
        bb_df = BollBand(stock_data=stock_data)
        reached_lower_bound = self._BBAND_count_in_range(bb_df=bb_df, price_df=price_df, lower_bound=True)
        reached_upper_bound = self._BBAND_count_in_range(bb_df=bb_df, price_df=price_df, lower_bound=False)

        if reached_lower_bound:
            stock_result.add_signal(indicator="BBAND", signal=Indicator_Signal.Bullish)
        elif reached_upper_bound:
            stock_result.add_signal(indicator="BBAND", signal=Indicator_Signal.Bearish)
        
        return 
        
    
    def _BBAND_count_in_range(self, bb_df: pd.DataFrame, price_df: pd.DataFrame, lower_bound: bool, range: float=0.1) -> bool:

        current_price = price_df["close"].iloc[0]
        if lower_bound and current_price <= bb_df["BB_dn"].iloc[0] + (bb_df["BB_range"].iloc[0] * range):
            return True
        elif not lower_bound and current_price >= bb_df["BB_up"].iloc[0] - (bb_df["BB_range"].iloc[0] * range):
            return True
        else:
            return False

    
    def analyze_stock_MACD(self, stock_data: Stock_Data, stock_result: Stock_Result, periods_back: int=3):
        macd_df = MACD(stock_data = stock_data, days_back = None)
        result = self._MACD_line_crossed(macd_df=macd_df, periods_back=periods_back)
        if result == 1:
            stock_result.add_signal(indicator="MACD", signal=Indicator_Signal.Bullish)
        elif result == -1:
            stock_result.add_signal(indicator="MACD", signal=Indicator_Signal.Bearish)
        else:
            return

    
    def _MACD_line_crossed(self, macd_df: pd.DataFrame, periods_back: int) -> int:
        '''
        Returns -1 if it is a downward trend, 1 if it is upward trend, 0 if no trend
        '''

        # Determine if the Signal Line and MACD line crossed each other
        periods_back_df = macd_df.iloc[:periods_back]
        
        start_macd = periods_back_df['MACD'].iloc[periods_back - 1]
        start_signal = periods_back_df['Signal'].iloc[periods_back - 1]

        end_macd = periods_back_df['MACD'].iloc[0]
        end_signal = periods_back_df['Signal'].iloc[0]
        
        #cutting down from top
        if start_macd >= start_signal and end_macd <= end_signal:
            return -1
        elif start_macd <= start_signal and end_macd >= end_signal:
            return 1
        else:
            return 0
            
            
        