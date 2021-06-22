import pandas as pd

from ..Constants.constants import PORTFOLIO_FILE_NAME

class Data_Reader:
    def read_excel(path: str="") -> pd.DataFrame:
        try:
            df = pd.read_excel(path + PORTFOLIO_FILE_NAME + ".xlsx")        
        except Exception as e:
            print("Failed to read excel file")
            print(e)
            return None
        return df
    

    def read_csv(path: str="") -> pd.DataFrame:
        try:
            df = pd.read_csv(path + PORTFOLIO_FILE_NAME + ".csv")        
        except Exception as e:
            print("Failed to read csv file")
            print(e)
            return None
        return df
        