import pandas as pd
import numpy as np

from ..Stock_Data_Acquisition.AlphaV_Stock_Data import Stock_Data


def RSI(stock_data: Stock_Data, days_back: int=None, n: int=20, drop_irrelavent: bool=True):
    '''
    The RSI is a basic measure of how well a stock is performing 
    against itself by comparing the strength of the up days versus the down days. 
    This number is computed and has a range between 0 and 100.  
    A reading above 70 is considered bullish, while a reading below 30 is an indication of bearishness.

    https://tradingsim.com/blog/relative-strength-index/
    '''
    if days_back is not None:
        price_df = reverse(stock_data.get_days_back(days=days_back)).copy()
    else:
        price_df = reverse(stock_data.get_dataframe()).copy()

    rsi_df = pd.DataFrame()
    rsi_df["delta"] = price_df["close"] - price_df["close"].shift(1)
    rsi_df["gain"] = np.where(rsi_df["delta"] >= 0, rsi_df["delta"], 0)
    rsi_df["loss"] = np.where(rsi_df["delta"] < 0, abs(rsi_df["delta"]), 0)
    avg_gain = []
    avg_loss = []

    gain = rsi_df["gain"].tolist()
    loss = rsi_df["loss"].tolist()

    for i in range(rsi_df.shape[0]):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(rsi_df["gain"].rolling(n).mean().tolist()[n])
            avg_loss.append(rsi_df["loss"].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n - 1) * avg_gain[i - 1] + gain[i])/n)
            avg_loss.append(((n - 1) * avg_loss[i - 1] + loss[i])/n)
        
    rsi_df["avg_gain"] = np.array(avg_gain)
    rsi_df["avg_loss"] = np.array(avg_loss)
    rsi_df["RS"] = rsi_df["avg_gain"]/rsi_df["avg_loss"]
    rsi_df["RSI"] = 100 - (100 / (rsi_df["RS"] + 1))

    if drop_irrelavent:
        rsi_df = rsi_df.drop(["avg_gain", "avg_loss", "RS", "delta", "gain", "loss"], axis = 1)
    
    return reverse(rsi_df)

def reverse(df: pd.DataFrame) -> pd.DataFrame:
    return df[::-1]



'''
Example Output

            delta  gain  loss  avg_gain  avg_loss        RS        RSI
date                                                                  
2020-11-27   0.56  0.56  0.00  1.083732  1.743649  0.621531  38.329886
2020-11-25   0.86  0.86  0.00  1.111297  1.835420  0.605473  37.713049
2020-11-24   1.32  1.32  0.00  1.124523  1.932021  0.582045  36.790666
2020-11-23  -3.49  0.00  3.49  1.114235  2.033706  0.547884  35.395663
2020-11-20  -1.30  0.00  1.30  1.172878  1.957059  0.599307  37.472901
...           ...   ...   ...       ...       ...       ...        ...
2020-07-15   2.67  2.67  0.00       NaN       NaN       NaN        NaN
2020-07-14   6.32  6.32  0.00       NaN       NaN       NaN        NaN
2020-07-13  -1.77  0.00  1.77       NaN       NaN       NaN        NaN
2020-07-10   0.67  0.67  0.00       NaN       NaN       NaN        NaN
2020-07-09    NaN  0.00  0.00       NaN       NaN       NaN        NaN
'''