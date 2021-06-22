from Modules.Portfolio_Acquisition.Portfolio_Data_Reader import Data_Reader

df = Data_Reader.read_excel()
print(df.iloc[0]["ticker"])