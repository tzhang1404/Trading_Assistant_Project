import unittest
import pandas as pd

from Modules.Portfolio_Acquisition.Portfolio_Data_Reader import Data_Reader
from Modules.Portfolio_Acquisition.Portfolio_Stock import Portfolio_Stock

class Test_Portfolio_Acquisition(unittest.TestCase):

    '''
        ticker  purchase_price purchase_date  shares  rules_increase_limit  rules_decrease_limit
    0   AAPL          210.15    2020-06-01      10                  0.10                   0.2
    1   ENPH          287.10    2020-06-18       8                  0.80                   0.5
    2     CD           35.12    2020-06-01      20                  0.15                   0.1
    3     ZM          300.13    2020-06-18       5                  0.20                   0.5
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_normal_excel_reading(self):
        df = Data_Reader.read_excel()
        self.assertEqual(df.shape[0], 4)
        self.assertEqual(df.shape[1], 6)
        self.assertEqual(df["ticker"][0], "AAPL")
        self.assertEqual(df["purchase_price"][0], 210.15)
        self.assertEqual(df["purchase_date"][0], pd.Timestamp("2020-06-01"))
        self.assertEqual(df["shares"][0], 10)
        self.assertEqual(df["rules_increase_limit"][0], 0.1)
        self.assertEqual(df["rules_decrease_limit"][0], 0.2)
    

    def test_normal_csv_reading(self):
        df = Data_Reader.read_csv()
        self.assertEqual(df.shape[0], 4)
        self.assertEqual(df.shape[1], 6)
        self.assertEqual(df["ticker"][0], "AAPL")
        self.assertEqual(df["purchase_price"][0], 210.15)
        self.assertEqual(pd.Timestamp(df["purchase_date"][0]), pd.Timestamp("2020-06-01"))
        self.assertEqual(df["shares"][0], 10)
        self.assertEqual(df["rules_increase_limit"][0], 0.1)
        self.assertEqual(df["rules_decrease_limit"][0], 0.2)
        

class Test_Portfolio_Stock(unittest.TestCase):

    '''
        ticker  purchase_price purchase_date  shares  rules_increase_limit  rules_decrease_limit
    0   AAPL          210.15    2020-06-01      10                  0.10                   0.2
    1   ENPH          287.10    2020-06-18       8                  0.80                   0.5
    2     CD           35.12    2020-06-01      20                  0.15                   0.1
    3     ZM          300.13    2020-06-18       5                  0.20                   0.5
    '''

    def setUp(self):
        self.df = Data_Reader.read_excel()

    def tearDown(self):
        pass


    def test_initialize_Portfolio_Stock_from_series(self):
        df_row = self.df.iloc[0]
        ps = Portfolio_Stock.from_pd_series(df_row)
        self.assertEqual(ps.ticker, df_row["ticker"])
        self.assertEqual(ps.purchase_date, df_row["purchase_date"])
        self.assertEqual(type(ps.purchase_date), pd.Timestamp)
    
    def test_initialize_Portfolio_Stock_from_dataframe(self):
        ps = Portfolio_Stock.from_pd_dataframe(df=self.df, row_index=0)
        self.assertEqual(ps.ticker, self.df["ticker"][0])
        self.assertEqual(ps.purchase_date, self.df["purchase_date"][0])
        self.assertEqual(type(ps.purchase_date), pd.Timestamp)

if __name__ == '__main__':
    unittest.main()