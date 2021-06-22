import pandas as pd

class Data_Reader:
    
    PORTFOLIO_FILE_NAME = "My_Portfolio"

    def read_excel(path: str="") -> pd.DataFrame:
        try:
            df = pd.read_excel(path + Data_Reader.PORTFOLIO_FILE_NAME + ".xlsx")        
        except Exception as e:
            print("Failed to read excel file")
            print(e)
            return None
        return df
    

    def read_csv(path: str="") -> pd.DataFrame:
        try:
            df = pd.read_csv(path + Data_Reader.PORTFOLIO_FILE_NAME + ".csv")        
        except Exception as e:
            print("Failed to read csv file")
            print(e)
            return None
        return df
        