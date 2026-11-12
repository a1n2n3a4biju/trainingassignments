import pandas as  pd
df=pd.read_csv('urban_mobility.csv')

# print(df.head(5))

# df["Energy_Per_Km"]=df["Energy_Used_kWh"]/df["Distance_Km"]
# print(df)

# print(df[(df["Vehicle_Type"]=="Electric Van") & (df["Maintenance_Flag"]=="Yes")])

print(df.groupby("Vehicle_Type").agg({
    "Distance_Km":"mean",
    "Trips_Count":"sum",
})
)

import numpy as np
# print("Mean:",np.mean(df["Energy_Used_kWh"]))
# print("Maximum:",np.max(df["Energy_Used_kWh"]))
# print("Minimum:",np.min(df["Energy_Used_kWh"]))

# import matplotlib.pyplot as plt
# vehicles=df.groupby("Vehicle_Type")["Energy_Used_kWh"].mean()
# vehicles.plot(kind="bar")
# plt.xlabel("Vehicle_Type")
# plt.ylabel("Energy Used (kWh)")
# plt.show()
