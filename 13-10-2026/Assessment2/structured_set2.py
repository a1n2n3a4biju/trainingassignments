import pandas as pd
df=pd.read_csv('renewable_energy.csv')

# print(df[(df["Energy_Type"]=="Solar") | (df["Energy_Type"]=="Wind")])
#
df["Efficiency_Percent"]=df["Actual_Output_MW"] / df["Capacity_MW"] *100


# print(df[df["Efficiency_Percent"]>85.00])

# print(df.groupby("Energy_Type")["Efficiency_Percent"].mean())

# print(df.groupby("Energy_Type")["Maintenance_Cost"].sum())

# print(df["Actual_Output_MW"].max())

df["Cost_Per_MW"]=df["Maintenance_Cost"] / df["Actual_Output_MW"]
# print(df)

# print(df.sort_values("Cost_Per_MW"))

# print(df[(df["Efficiency_Percent"]>80) & (df["Cost_Per_MW"]<70000)])

# import matplotlib.pyplot as plt
# efficiency=df.groupby("Plant_Name")["Efficiency_Percent"].sum()
# efficiency.plot(kind="bar")
# plt.xlabel("Plant_Name")
# plt.ylabel("Efficiency_Percent")
# plt.show()
