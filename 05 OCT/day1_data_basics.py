import pandas as pd
data = {
    "Product": ["Laptop", "Mouse", "Keyboard", "Laptop", "Mouse"],
    "City": ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Delhi"],
    "Quantity": [2, 5, 3, 1, 4],
    "Price": [60000, 800, 1500, 60000, 800]
}

df=pd.DataFrame(data)
#print(df.head())#only for top 5 rows
#print(df.shape)#to show size here(5,4)
#print(df.columns)
#print(df.dtypes)#to show datatype

#Data Manipulations

#print(df[df["City"] == "Hyderabad"])
#print(df[["Product","Price"]])
# Add a new column
df["Total"]=df["Quantity"]*df["Price"]
#print(df)

#print(df.groupby("Product")["Total"].sum())

#print(df.sort_values(by="Total", ascending=False))

#import matplotlib.pyplot as plt
#sales=df.groupby("Product")["Total"].sum()
#(sales.plot(kind="bar"))
#plt.title("Sales by Product")
#plt.xlabel("Product")
#plt.ylabel("Total Sales")
#plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(data=df, x="Department", y="Assessment_Score")

plt.title("Sales by Product")
plt.show()
