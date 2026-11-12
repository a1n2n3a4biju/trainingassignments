import pandas as pd
df=pd.read_csv('library_loans.csv')

print(df[["Member_Name","Book_Category","Fine"]]) # for 1 clm 1 sq bracket but for multiple columns 2 sq brakets

print(df[df["Fine"]>50])# inner df will convert each row into boolean and outer df will only filter true rows
import numpy as np
df["Status"]=np.where(df["Fine"]==0 ,"NO Fine", "Fine Due")
print(df)

print("Average:",df["Days_Borrowed"].mean())

print(df.groupby("Book_Category")["Fine"].sum())