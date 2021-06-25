from enum import Enum


PORTFOLIO_HEADERS = ["ticker", "purchase_price", "purchase_date", "shares", "rules_increase_limit", "rules_decrease_limit"]
# Sample row for portfolio: ["AAPL", "291.24", "2021-06-01", "10", "0.1", "0.1"]

PORTFOLIO_FILE_NAME = "My_Portfolio"

ALPHAVANTAGE_KEY = "R8WLI4V6VZGAFFMO"

IEXFINANCE_TOKEN = "sk_a9b4128fd41d43dd9f03d5a3a9e41d30"

#used to detect error message type
FREQUENCY_EXCEPTION_KEY_WORD = "call frequency"



class Interval(Enum):
    one_minute = '1min'
    five_minutes = '5min'
    thirty_minutes = '30min'
    one_hour = '60min'