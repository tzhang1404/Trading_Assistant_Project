# Trading Assistant Project (Completed)

Author: Jiawei Zhang [June, 2021]

To test run the project, make sure you populate the My_Portfolio.xlsx or My_Portfolio.csv file with tickers of you choice, and run 
following command in terminal

    python main.py

**Project Overview**

The Trading Assistant Project (TAP) is designed to monitor the performance of my stocks. By tracking a list Robinhood portfolios, TAP can alert users whether if the stock price is within his/her investment strategy, track the performance of different stocks, and provide rudimentary technical analysis results with simple indicators. The goal of the project is not to make trades or to automate the process of decision making, but to serve as an assistant for the user so that the user can set a pre-determined investment rule/thesis and execute the final sell strictly based on how he/she set up the rules. TAP will help the user avoid emotional sell-off by forcing the user to abide by the investment rules, while the technical analysis indicators can help users identify potential buy-ins or sell-offs.

The technical indicators used in this project includes: RSI, MACD, Bollinger Bands

**Project Deliverable**

The project deliverable will contain a python program that takes in a form of portfolio record (excel, csv, Robinhood) with the optional information of purchase date, price, sell-off point, and any other additional rules that can be used to monitor the portfolio performance. The python program will then produce a form of notification (email, text, console output) for the users on a daily basis that will include the performance of the portfolio and whether any actions needs to be taken on the portfolio. The python program should be lightweight, easily maintained, and easily expandable, with a focus on portfolio acquisition method, investment rules expansion, and notification methods.

**Project Timeline and Milestones**

**Milestone 1: Project Module Setup and Portfolio Acquisition Module (Completed on June 22, 2021)**

Milestone 1 should prepare project repository and understand how to properly setup Python projects with easy imports and modulations. Once the project is setup, build the portfolio acquisition module designed to consume and parse local data stored in csv or excel. All portfolio data should be stored in respective data structures along with investment rules

1. Repo setup and project setup (Design data structures)
2. Learn about Python modules
3. Prepare management of packages (Pandas and such)
4. Create portfolio acquisition module

**Milestone 2: OHLC Data Acquisition Module (Week 2)**

Milestone 2 will resemble earlier projects of trading bot and should obtain stock price data (hourly or daily) based on the portfolio data extracted in milestone 1. The OHLC data should be stored with the portfolio stock data for later analysis

1. Setup OHLC acquisition module
2. Provide API to acquire daily or more fine-grained data
3. Store data in respective data structures

**Milestone 3a: Data Analysis Module (Performance Monitoring) (Week 3)**

Milestone 3a should focus on performance monitoring-checking whether the stocks in my portfolio is performing according to user&#39;s expectation. If a stock has risen above or dropped below the highest or lowest sell-limit set by the user, a notification should be created for that stock.

1. Design analysis algorithm
2. Create notification data structure for stocks
3. Create data structure for storing notifications (taking into account of later technical analysis results)
4. Ability to use either a daily data or an intraday data.

**Milestone 3b: Data Analysis Module (Technical Analysis) (Week 3)**

Milestone 3b will reuse some of the code that I have built before, but with a more simplified choice of indicators (prob 2-3 indicators). The raw result should be provided along with a calculated score for easy understanding.

1. Refactor indicator code from trading bot project
2. Add results to notification data structure
3. Ability to consume either daily data or intraday data.

**Milestone 4: Notification Delivery Module (Email) (Week 4)**

Milestone 4 will mostly be uncharted territory for me, and the goal is to use all the results and notification data we had from milestone 3 to generate a textual email that contains vital information of the portfolio, whether to sell or closely monitor any stocks.

1. Extract results and notification data
2. Generate and format text string
3. Use email packages to send out the email

**Milestone 5: Automation Module (Week 4, 5)**

The entire project is now running on AWS EC2 t2.tiny machine, with a scheduled cronjob to run twice everyday. The first excution will take place 30 mins after the market opens and the second execution will take place 30 mins before the market closes. This design is to give time to the user (myself) time to act if there is an action recommended to me. 

**Milestone 6: Portfolio Research and Selection (Week 5)**
Completed at my own discretion. 