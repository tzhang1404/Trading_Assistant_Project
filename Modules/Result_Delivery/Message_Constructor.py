
import datetime
from pytz import timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

from ..Performance_Monitoring.Stock_Performance import Stock_Performance, Stock_Performance_Collection
from ..Constants.constants import SENDER_EMAIL, RECEIVER_EMAILS, Stock_Action


class Message_Constructor():

    def __init__(self, sp_collection: Stock_Performance_Collection):
        self.sp_collection = sp_collection
        self.msg_list = []

        sp_list = self.sp_collection.get_all_stock_performances()
        stock_performance = sp_list[0]
        
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

        html = f"""\
                <html>
                <body>
                    <h2>Stock Performance for {datetime.date.today()}</h2>
                    <h4>Please update myPortfolio spreadsheet data if actions are executed</h4>
                    {Message_Constructor.generate_stock_message(sp_list)}
                </body>
                </html>
                """
        msg_component = MIMEText(html, "html")
        message.attach(msg_component)

        self.msg_list.append(message)

    @staticmethod
    def generate_stock_message(sp_list: List[Stock_Performance]) -> str:
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
        return res_string
    
    @staticmethod
    def _get_stock_action_font_style(action: Stock_Action) -> str: 
        if action == Stock_Action.LOSS_SELL:
            return "background-color:red;color:white;"
        elif action == Stock_Action.PROFIT_SELL:
            return "background-color:green;color:white;"

    @staticmethod
    def _get_correct_sell_limit(sp: Stock_Performance) -> float:
        action = sp.get_action_result()
        if action == Stock_Action.LOSS_SELL:
            return sp.portfolio_data.decrease_limit
        elif action == Stock_Action.PROFIT_SELL:
            return sp.portfolio_data.increase_limit


    def get_message(self) -> str:
        return self.msg_list[0].as_string()            
            
    
