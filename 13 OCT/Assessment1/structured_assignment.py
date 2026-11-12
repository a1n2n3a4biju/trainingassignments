import pandas as pd
from pandas.conftest import ascending

df=pd.read_csv("structured_data.csv")

# print(df[["Shipment_ID","Origin","Destination","Cost"]])
#
# print(df[df["Mode"]=="Road"])

# print(df[df["Weight_Kg"]>150])

# df["Cost_Per_Km"]=df["Cost"]/df["Distance_Km"]
# print(df)

import numpy as np
# print("Average",np.average(df["Cost"]))
# print("Highest",np.max(df["Cost"]))
# print("Lowest",np.min(df["Cost"]))

# print(df.groupby("Mode")["Cost"].sum())

# print(df.groupby("Mode")["Weight_Kg"].mean())

# print(df.sort_values(by=["Cost"], ascending=False))

# print(df[(df["Delivery_Days"]<=1) & (df["Cost"]<5000)])