import json
with open('equipment_events.json') as json_file:
    events = json.load(json_file)

# for event in events:
#     print(event["event_id"],event["asset"]["type"],event["asset"]["site"],event["severity"])



for event in events:
    if event["temperature"] > 70:
        print(event.get("actions","No actions recorded"))



