import pandas as pd

from ..Stock_Data_Acquisition.AlphaV_Stock_Data import Stock_Data


def MACD(stock_data: Stock_Data, days_back: int=None, fast_n: int=12, slow_n: int=26, drop_irrelavent: bool=True) -> pd.DataFrame:
    '''
    MACD cutting Signal from bottom -> Upward Trend
    MACD cutting Signal from top -> downward Trend
    A lagging indicator -> the indicator will be significant only after a trend has already happened
    Too simple, has a lot of false positive. So it has to be used in conjunction with other indicators
    '''
    if days_back is not None:
        price_df = reverse(stock_data.get_days_back(days=days_back)).copy()
    else:
        price_df = reverse(stock_data.get_dataframe()).copy()

    macd_df = pd.DataFrame()
    macd_df["MV_fast"] = price_df["close"].ewm(span = 12, min_periods = 12).mean()
    macd_df["MV_slow"] = price_df["close"].ewm(span = 26, min_periods = 26).mean()
    macd_df["MACD"] = macd_df["MV_fast"] - macd_df["MV_slow"]
    macd_df["Signal"] = macd_df["MACD"].ewm(span = 9, min_periods = 9).mean() 
    macd_df.dropna(inplace = True)
    if drop_irrelavent:
        macd_df = macd_df.drop(['MV_fast', 'MV_slow'], axis=1)
    return reverse(macd_df)



def reverse(df: pd.DataFrame) -> pd.DataFrame:
    return df[::-1]

'''
Example Output  (Flipped)
                         MACD    Signal
date                                   
2020-11-24 13:30:00  0.122997  0.031844
2020-11-24 14:00:00  0.200468  0.069626
2020-11-24 14:30:00  0.212504  0.100887
2020-11-24 15:00:00  0.241003  0.130978
2020-11-24 15:30:00  0.284422  0.163452
...                       ...       ...
2020-11-27 12:30:00  0.193901  0.243740
2020-11-27 13:00:00  0.162329  0.227458
2020-11-27 13:30:00  0.134945  0.208955
2020-11-27 16:30:00  0.104777  0.188120
2020-11-27 17:00:00  0.075163  0.165528
'''