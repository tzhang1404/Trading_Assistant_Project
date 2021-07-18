
import datetime
from pytz import timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

from ..Performance_Monitoring.Stock_Performance import Stock_Performance, Stock_Performance_Collection
from ..Technical_Indicators.Indicator_Results import Stock_Result, Stock_Result_Storage
from ..Constants.constants import Indicator_Signal, SENDER_EMAIL, RECEIVER_EMAILS, Stock_Action


class Message_Constructor():

    def __init__(self, sp_collection: Stock_Performance_Collection, tech_indicator_collection: Stock_Result_Storage):
        self.sp_collection = sp_collection
        self.action_msg = None
        self.performance_msg = None

        sp_list = self.sp_collection.get_all_stock_performances()

        message = Message_Constructor.generate_message_metadata()

        action_msg = Message_Constructor.generate_stock_action_message(sp_list) 
        if action_msg == "":
            action_msg = "No Stock Action Today"

        performance_msg = Message_Constructor.generate_raw_performance_message(sp_list)

        technical_msg = Message_Constructor.generate_technical_analysis_message(tech_indicator_collection)

        html = f"""\
                <html>
                <body>
                    <h2>Stock Performance for {datetime.date.today()}</h2>
                    <h3>--Portfolio Action Result--</h3>
                    {action_msg}
                    <h3>--Portfolio Performance Result--</h3>
                    {performance_msg}
                    <h3>--Watchlist Technical Analysis Result--</h3>
                    {technical_msg}
                </body>
                </html>
                """
        msg_component = MIMEText(html, "html")
        message.attach(msg_component)

        self.action_msg = message

    @staticmethod
    def generate_message_metadata():
        message = MIMEMultipart("alternative")
        hourtime_NY = int(datetime.datetime.now(timezone('America/New_York')).strftime("%H"))
        if hourtime_NY < 12:
            message["Subject"] = "TAP Morning Stock Monitoring Result"
        elif hourtime_NY >= 12:
            message["Subject"] = "TAP Afternoon Stock Monitoring Result"
        else: 
            message["Subject"] = "TAP ??? Stock Monitoring Result"

        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAILS[0]

        return message

    @staticmethod
    def generate_raw_performance_message(sp_list: List[Stock_Performance]) -> str: 
        res_string = "<p>"
        for sp in sp_list:
            price_delta = sp.price_delta.rt_price_delta
            res_string += f"""
                        <strong>{sp.get_ticker()}</strong><br>
                        Price Delta Since Purchase: <span style={Message_Constructor._get_stock_delta_style(price_delta)}> {round(100 * price_delta, 2)}% </span><br>
                        Capital Gain/Loss: ${round(price_delta * sp.portfolio_data.purchase_price * sp.portfolio_data.shares, 2)} <br>
                        <br>
                        """
        res_string += "</p>"
        return res_string


    @staticmethod
    def generate_stock_action_message(sp_list: List[Stock_Performance]) -> str:
        res_string = "<p>"
        for sp in sp_list:
            action = sp.get_action_result()
            if action is not None:
                res_string += f"""
                                <strong>{sp.get_ticker()}</strong><br>
                                Result: <span style={Message_Constructor._get_stock_action_font_style(action)}>{action}</span> <br>
                                Current Price: ${sp.rt_price_data.price} <br>
                                Price Delta: {round(sp.price_delta.rt_price_delta * 100, 2)}%<br>
                                Estimated Capital Gain: ${round(sp.price_delta.rt_price_delta * sp.portfolio_data.purchase_price * sp.portfolio_data.shares, 2)}<br>
                                <br>
                            """
        res_string += "</p>"
        if res_string == "<p></p>":
            res_string = ""
        return res_string

    
    @staticmethod
    def generate_technical_analysis_message(technical_result_collection: Stock_Performance_Collection) -> str:
        res = "<p>"
        for ticker, result in technical_result_collection.result_dict.items():
            res += f"""
                    <strong>{ticker}</strong> 
                    RSI: <span style={Message_Constructor._get_indicator_style(result.get_signal_result("RSI"))}> {result.get_signal_result_str("RSI")} </span> <br>
                    MACD: <span style={Message_Constructor._get_indicator_style(result.get_signal_result("MACD"))}> {result.get_signal_result_str("MACD")} </span> <br>
                    BBAND: <span style={Message_Constructor._get_indicator_style(result.get_signal_result("BBAND"))}> {result.get_signal_result_str("BBAND")} </span> <br>
                    <br>
                """
        res += "</p>"
        if res == "<p></p>":
            res = ""
        return res
    
    @staticmethod
    def _get_stock_action_font_style(action: Stock_Action) -> str: 
        if action == Stock_Action.LOSS_SELL:
            return "background-color:red;color:white;"
        elif action == Stock_Action.PROFIT_SELL:
            return "background-color:green;color:white;"

    @staticmethod
    def _get_stock_delta_style(value: float) -> str: 
        if value < 0:
            return "background-color:red;color:white;"
        else:
            return "background-color:green;color:white;"

    @staticmethod
    def _get_indicator_style(signal: Indicator_Signal) -> str:
        if signal == Indicator_Signal.Bearish:
            return "background-color:red;color:white;"
        elif signal == Indicator_Signal.Bullish:
            return "background-color:green;color:white;"


    @staticmethod
    def _get_correct_sell_limit(sp: Stock_Performance) -> float:
        action = sp.get_action_result()
        if action == Stock_Action.LOSS_SELL:
            return sp.portfolio_data.decrease_limit
        elif action == Stock_Action.PROFIT_SELL:
            return sp.portfolio_data.increase_limit


    def get_action_message(self) -> str:
        if self.action_msg is None:
            return ""
        else:
            return self.action_msg.as_string()            
            
    
