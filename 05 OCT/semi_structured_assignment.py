import json
with open("festival_events.json") as file:
    events=json.load(file)

for event in events:
    print(event["name"])

for event in events:
    print(event["location"]["city"])

for event in events:
    if event["visitors"]>700:
        print(event)
for event in events:
    print(event.get("features","No features listed"))

import pandas as pd
data=pd.json_normalize(events)