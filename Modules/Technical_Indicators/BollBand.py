import pandas as pd

from ..Stock_Data_Acquisition.AlphaV_Stock_Data import Stock_Data

def BollBand(stock_data: Stock_Data, days_back: int=None, n: int=20, drop_irrelavent: bool=True) -> pd.DataFrame:
    """
    https://www.investopedia.com/trading/using-bollinger-bands-to-gauge-trends/
    Used to identify overbought and oversold conditions, price breaking below the lower bound signals oversold
    and vice versa

    The function returns the BollBand dataframe with Upper and Longer Bound, 
    but does not perform any analysis
    """
    if days_back is not None:
        price_df = stock_data.get_days_back(days=days_back).copy()
    else:
        price_df = stock_data.get_dataframe().copy()

    bb_df = calculate_typical_price(bb_df=pd.DataFrame(), price_df=price_df)
    bb_df["MA"] = price_df["close"].rolling(n).mean()
    bb_df["BB_up"] = bb_df["MA"] + 2 * bb_df["MA"].rolling(n).std()
    bb_df["BB_dn"] = bb_df["MA"] - 2 * bb_df["MA"].rolling(n).std()
    bb_df["BB_range"] = bb_df["BB_up"] - bb_df["BB_dn"]
    bb_df.dropna(inplace=True)

    if drop_irrelavent:
        bb_df = bb_df.drop(["MA", "TP"], axis=1)

    return bb_df


def calculate_typical_price(bb_df: pd.DataFrame, price_df: pd.DataFrame) -> pd.DataFrame:
    bb_df["TP"] = round((price_df["close"] + price_df["high"] + price_df["low"]) / 3, 3)
    return bb_df

'''
Example Output

                 TP        MA       BB_up       BB_dn    BB_range
date                                                             
2020-10-05  115.567  116.5640  117.144368  115.983632    1.160737
2020-10-02  113.537  116.7720  117.435772  116.108228    1.327543
2020-10-01  116.780  116.8455  117.600668  116.090332    1.510336
2020-09-30  115.563  117.0760  117.960445  116.191555    1.768890
2020-09-29  114.323  116.9505  117.913556  115.987444    1.926111

'''