
from fastapi import FastAPI, HTTPException

from schemas import TripCreate, ChatRequest

from tools.trip_tools import create_trip, get_trip_details

from assistant.workflow import generate_travel_advisory


# PART 1: Create FastAPI application
app = FastAPI(
    title="AI Travel and Weather Advisory Assistant",
    description="An AI assistant for employee travel planning",
    version="1.0"
)


# PART 2: Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Travel and Weather Advisory Assistant"
    }


# PART 3: Health endpoint
@app.get("/health")
def health():
    return {
        "status": "API is running"
    }


# PART 4: Create a new trip
@app.post("/trips")
def register_trip(trip: TripCreate):

    try:
        trip_id = create_trip(
            trip.employee_id,
            trip.destination,
            trip.start_date,
            trip.end_date,
            trip.purpose
        )

        return {
            "message": "Trip registered successfully",
            "trip_id": trip_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# PART 5: Retrieve trip details
@app.get("/trips/{trip_id}")
def retrieve_trip(trip_id: int):

    trip = get_trip_details(trip_id)

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    return trip


# PART 6: Chat with AI assistant
@app.post("/chat")
def chat_with_assistant(request: ChatRequest):

    try:
        answer = generate_travel_advisory(
            request.trip_id,
            request.session_id,
            request.question
        )

        return {
            "trip_id": request.trip_id,
            "session_id": request.session_id,
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
