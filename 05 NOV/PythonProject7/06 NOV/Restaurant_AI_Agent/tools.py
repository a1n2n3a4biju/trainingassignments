
import json
from pathlib import Path
from langchain.tools import tool

FILE = Path(__file__).parent / "restaurants.json"


def get_restaurants():
    return json.loads(FILE.read_text(encoding="utf-8"))


@tool
def search_restaurants(keyword: str) -> str:
    """Search restaurants using cuisine, name or location."""

    matches = [
        r for r in get_restaurants()
        if keyword.lower() == r["cuisine"].lower()
        or keyword.lower() == r["name"].lower()
        or keyword.lower() == r["location"].lower()
    ]

    return json.dumps(matches)


@tool
def calculate_dining_cost(restaurant_id: str, guests: int) -> str:
    """Calculate the dining cost of a restaurant."""

    if guests<1 or guests>20:
        return "Booking is allowed for 20 people only"

    for r in get_restaurants():
        if str(r["id"]) == str(restaurant_id):

            total_cost = r["price_per_person"] * guests

            return json.dumps({
                "restaurant": r["name"],
                "guests": guests,
                "total_cost": total_cost,
                "cuisine": r["cuisine"],
                "location": r["location"]
            })

    return "Restaurant not found"
