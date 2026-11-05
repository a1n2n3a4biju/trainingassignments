
import json
from pathlib import Path
from langchain.tools import tool

FILE = Path(__file__).parent / "workshops.json"
COUPON_FILE = Path(__file__).parent / "coupons.json"

def get_workshops():
    return json.loads(FILE.read_text(encoding="utf-8"))

def get_coupons():
    return json.loads(COUPON_FILE.read_text(encoding="utf-8"))



@tool
def search_workshops(keyword: str) -> str:
    """Search available workshops by title."""

    matches = [
        w for w in get_workshops()
        if keyword.lower() in w["title"].lower()
    ]

    return json.dumps(matches)



@tool
def find_cheapest_workshop():
    """Find and return the workshop with the lowest fee."""
    workshops = get_workshops()

    if not workshops:
        return "No workshops available."

    cheapest = min(workshops, key=lambda workshop: workshop["fee"]  )

    return cheapest



@tool
def calculate_workshop_fee(
    workshop_id: str,
    participants: int,
    coupon_code: str = ""
) -> str:
    """Calculate the workshop fee and apply a valid coupon discount."""

    if participants < 1 or participants > 30:
        return "Participant count must be between 1 and 30."

    workshop_id = workshop_id.strip().upper()
    coupon_code = coupon_code.strip().upper()

    for workshop in get_workshops():

        if workshop["id"].upper() == workshop_id:

            total = workshop["fee"] * participants
            discount = 0
            discount_percentage = 0
            coupon_message = "No coupon applied."

            if coupon_code:

                coupons = get_coupons()

                for coupon in coupons:

                    if coupon["code"].upper() == coupon_code:
                        discount_percentage = coupon["discount"]
                        discount = total * discount_percentage / 100
                        coupon_message = "Coupon discount applied."
                        break

                else:
                    coupon_message = "Invalid coupon code."

            final_fee = total - discount

            return json.dumps({
                "workshop": workshop["title"],
                "participants": participants,
                "original_fee": total,
                "coupon_code": coupon_code or None,
                "discount_percentage": discount_percentage,
                "discount_amount": discount,
                "coupon_message": coupon_message,
                "final_fee": final_fee
            })

    return "Workshop not found."



if __name__ == "__main__":
    print(search_workshops.invoke({"keyword": "Python"}))

    print(calculate_workshop_fee.invoke({
        "workshop_id": "W101",
        "participants": 4
    }))
