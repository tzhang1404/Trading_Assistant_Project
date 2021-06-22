from Modules.Portfolio_Acquisition.Portfolio_Data import Portfolio_Data
# from Modules.Portfolio_Acquisition.Portfolio_Stock import Portfolio_Stock



def main():
    portfolio_data = Portfolio_Data.from_reading_data()
    print(portfolio_data.get_all_stocks())

main()