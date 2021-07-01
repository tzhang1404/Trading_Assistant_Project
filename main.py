from typing import List

from Modules.Portfolio_Acquisition.Portfolio_Stock_Collection import Portfolio_Stock_Collection as Portfolios
from Modules.Stock_Data_Acquisition.IEX_Stock_Query import IEX_Stock_Query
from Modules.Performance_Monitoring.Stock_Performance import Stock_Performance_Collection as Performances
from Modules.Result_Delivery.Email_Sender import Email_Sender
from Modules.Result_Delivery.Message_Constructor import Message_Constructor

def main():
    portfolio_stock_collection = Portfolios.from_reading_data()
    stock_price_collection =IEX_Stock_Query.query_multiple_realtime_prices(tickers=portfolio_stock_collection.get_all_tickers())
    performance_result_collection = Performances.analyze_all_realtime_price(
        port_collection=portfolio_stock_collection, 
        price_collection=stock_price_collection)
    # performance_result_collection.debug_print_all_performance_result()
    email_sender = Email_Sender()
    msg_constructor = Message_Constructor(sp_collection=performance_result_collection)
    message = msg_constructor.get_message()
    email_sender.send_message(msg=message)
    

    

    
    

main()