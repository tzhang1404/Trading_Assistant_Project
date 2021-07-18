from typing import Dict

from ..Constants.constants import Notification, Indicator_Signal


class Stock_Result():
    """
    Class for holding analysis results of a stock
    """

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.signals = {} # signal from different indicators
    
    def add_signal(self, indicator: str, signal: Indicator_Signal):
        self.signals[indicator] = signal

    def get_all_signals(self) -> Dict:
        return self.signals
    
    def get_signal_result(self, signal_type: str) -> Indicator_Signal:
        if signal_type in self.signals:
            return self.signals[signal_type]
        else:
            return None
 
    def get_signal_result_str(self, signal_type: str) -> str:
        if signal_type in self.signals:
            if self.signals[signal_type] == Indicator_Signal.Bearish:
                return "Bearish"
            elif self.signals[signal_type] == Indicator_Signal.Bullish:
                return "Bullish"
        else:
            return "None"

class Stock_Result_Storage():
    
    def __init__(self):
        self.result_dict = {}
        self.tickers = []
    
    def add_result(self, stock_result: Stock_Result):
        ticker = stock_result.ticker
        self.result_dict[ticker] = stock_result
        if not ticker in self.tickers:
            self.tickers.append(ticker)
    
    def get_result(self, ticker: str) -> Stock_Result:
        if not ticker in self.result_dict:
            raise ValueError(f"Looking for a non-existent stock result {ticker}")
        return self.result_dict[ticker]
    
    def get_tickers(self):
        return self.tickers
