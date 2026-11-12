import pandas as pd
data = {
    "Employee": ["Aisha", "Rahul", "Neha", "Omar", "Priya", "Karan", "Fatima", "Vikram"],
    "Department": ["HR", "IT", "Finance", "IT", "HR", "Finance", "IT", "HR"],
    "Training_Hours": [12, 18, 10, 22, 15, 8, 20, 14],
    "Assessment_Score": [78, 88, 72, 91, 84, 69, 95, 80],
    "Completed": ["Yes", "Yes", "No", "Yes", "Yes", "No", "Yes", "Yes"]
}

df = pd.DataFrame(data)
print(df)
print(df.head(4))
print(df[["Employee","Assessment_Score"]])
print(df[df["Department"]=="IT"])
print(df[df["Assessment_Score"]>80])
print(df[df["Completed"]=="Yes"])
print(df[(df["Department"]=="IT") & (df["Assessment_Score"]>85)])
import numpy as np
df["Passed"]=np.where(df["Assessment_Score"]>=75 ,"Pass","Fail")
print(df)
print("Average Assessment:",np.average(df["Assessment_Score"]))
print("Highest:",np.max(df["Assessment_Score"]))
print("Lowest:",np.min(df["Assessment_Score"]))
print("Average Training:",np.average(df["Training_Hours"]))
print(df.sort_values(by="Assessment_Score", ascending=False))
print(df.groupby("Department")["Assessment_Score"].mean())
print(df.groupby("Department")["Training_Hours"].sum())
print(df.groupby("Department").size())
print((df["Completed"]=="Yes").sum())
scores = df["Assessment_Score"].to_numpy()
print("mean:",np.mean(scores))
print("maximum:",np.max(scores))
print("minimum:",np.min(scores))
print("std_deviation:",np.std(scores))

#import matplotlib.pyplot as plt
#sales=df.groupby("Department")["Assessment_Score"].mean()
#(sales.plot(kind="bar"))
#plt.title("Score by Department")
#plt.xlabel("Department")
#plt.ylabel("Score")
#plt.show()
import matplotlib.pyplot as plt
sales=df.groupby("Department")["Training_Hours"].sum()
(sales.plot(kind="bar"))
plt.title("Training Hours by Department")
plt.xlabel("Department")
plt.ylabel("Training Hours")
plt.show()

import seaborn as sns

import matplotlib.pyplot as plt

sns.barplot(data=df, x="Department", y="Assessment_Score")

plt.title("Department by Assessment Score")
plt.show()