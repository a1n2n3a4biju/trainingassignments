import json
with open("semistructured_data.json") as f:
    incidents=json.load(f)
#
# for incident in incidents:
#     print(incident["incident_id"])

# for incident in incidents:
#     print(incident["location"]["city"])
#
# for incident in incidents:
#     if incident["severity"]=="High":
#         print(incident)
#
# for incident in incidents:
#     if incident["category"]=="Safety":
#         print(incident)

# for incident in incidents:
#     print(incident.get("actions","No actions recorded"))

# from collections import Counter
# print(Counter(incident["severity"] for incident in incidents))

# for incident in incidents:
#     incident["status"]="open"
# print(incidents)

# with open("updated_incidents.json","w") as f:
#     json.dump(incidents,f, indent=4)
# print("Updated records r saved")
import pandas as pd
data=pd.json_normalize(incidents)

print(data[["incident_id","severity","category","location.city","location.site"]])