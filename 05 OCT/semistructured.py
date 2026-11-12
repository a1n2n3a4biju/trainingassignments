import json
import pandas as pd
with open('support_tickets.json') as file:
    tickets = json.load(file)
df=pd.json_normalize(tickets)
print(df)
#print(tickets)
#print(tickets[0])
#print(tickets[0]["issue"])
#print(tickets[0]["customer"]["name"])

#for ticket in tickets:
    #print(ticket["ticket_id"],ticket["issue"])

#print(tickets[1]["priority"])
#print(tickets[1].get("priority","Not Assigned"))