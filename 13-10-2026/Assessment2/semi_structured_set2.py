import json
with open("smart_homes.json") as f:
    devices=json.load(f)

# for device in devices:
#     print(device["device_id"],device["device_type"],device["room"])

# for device in devices:
#     if device["status"]=="Active":
#         print(device)

# for device in devices:
#     if device["metrics"]["battery"]<60:
#         print(device)

# for device in devices:
#     print(device.get("metrics",{}).get("temperature"))


# for device in devices:
#     if device.get("alerts"):
#         print(device)


# from collections import Counter
# print(Counter(device["device_type"] for device in devices))

for device in devices:
    if device["metrics"]["battery"]>=70:
        device["health"]="Good"
    elif (device["metrics"]["battery"]>50) & (device["metrics"]["battery"]<69):
        device["health"]="Moderate"
    else:
        device["health"]="Low"
# print(devices)

with open("device_health_report.json","w") as f:
    json.dump(devices,f,indent=4)
# print("Json is updated successfully")

import pandas as pd
df=pd.json_normalize(devices)
# print(df[["device_id","device_type","room","status","metrics.battery","health"]])

print(df[(df["status"]=="Active") & (df["metrics.battery"]<70)])






