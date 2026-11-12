import pandas as pd
df=pd.read_csv("ev_sessions.csv")
print(df)
print(df.columns)
print(df.shape)
print(df.dtypes)
print(df[["Station","kWh","Amount"]])
