
import psycopg2
from tools.weather_tools import get_coordinates, get_weather
from langchain_core.tools import tool

def get_connection():

    return psycopg2.connect(
        host="localhost",
        database="travel_weather_db",
        user="postgres",
        password="Admin@123"
    )


def create_trip(employee_id, destination, start_date, end_date, purpose):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trips
        (employee_id, destination, start_date, end_date, purpose)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING trip_id
    """, (employee_id, destination, start_date, end_date, purpose))

    trip_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return trip_id

def get_trip_details(trip_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM trips
        WHERE trip_id = %s
    """, (trip_id,))

    trip = cursor.fetchone()

    cursor.close()
    conn.close()

    if trip is None:
        return None

    return {
        "trip_id": trip[0],
        "employee_id": trip[1],
        "destination": trip[2],
        "start_date": str(trip[3]),
        "end_date": str(trip[4]),
        "purpose": trip[5],
        "status": trip[6]
    }


def get_trip_weather(trip_id):

    # STEP 1: Retrieve the trip
    trip = get_trip_details(trip_id)

    if trip is None:
        return {
            "error": "Trip not found"
        }

    # STEP 2: Get destination
    destination = trip["destination"]

    # STEP 3: Get travel dates
    start_date = trip["start_date"]
    end_date = trip["end_date"]

    # STEP 4: Get destination coordinates
    location = get_coordinates(destination)

    if location is None:
        return {
            "error": "Destination not found"
        }

    # STEP 5: Fetch weather
    weather = get_weather(
        location["latitude"],
        location["longitude"],
        start_date,
        end_date
    )

    if weather is None:
        return {
            "error": "Weather forecast unavailable"
        }

    # STEP 6: Return trip and weather details
    return {
        "trip": trip,
        "location": location,
        "weather": weather
    }



@tool
def trip_lookup_tool(trip_id: int):
    """Retrieve a registered employee trip using its trip ID."""

    trip = get_trip_details(trip_id)

    if trip is None:
        return {
            "error": "Trip not found"
        }

    return trip


# Test the function
if __name__ == "__main__":

    result = get_trip_weather(1)

    print("\nCOMPLETE TRAVEL INFORMATION")

    print(result)