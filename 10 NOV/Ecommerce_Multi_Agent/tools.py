import json
from pathlib import Path
from agent_framework import tool

FILE=Path(__file__).parent/"products.json"

def get_products():
    return json.loads(FILE.read_text(encoding="utf-8"))

@tool(approval_mode="never_require")
def search_product(keyword:str)->str:
    "to return a list of products matching the keyword"

    print(f"[TOOL CALLED] search_product: {keyword}")
    matches = [
        w for w in get_products()
        if keyword.lower() in w["name"].lower()
        or keyword.lower() in w["category"].lower()
    ]

    return json.dumps(matches)

@tool(approval_mode="never_require")
def calculate_order_total(prdct_id: str, quantity:int)->str:
    "to calculate the total amount of a product"
    print(f"[TOOL CALLED] calculate_order_total: {prdct_id}, {quantity}")
    if quantity<0 :
        return "invalid quantity"
    for p in get_products():
        if p['id'].upper() == prdct_id.upper():
            if p['stock']<quantity:
                return "sufficent stock is not present"
                break
            total_cost = quantity * p['price_inr']
            return json.dumps({
                    "id":p['id'],
                    "name":p['name'],
                    "category":p['category'],
                    "price":p['price_inr'],
                    "quantity":quantity,
                    "total_cost":total_cost,
                    "rating":p['rating']

                })
    return "product is not found"

