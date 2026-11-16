
from pydantic import BaseModel
from datetime import date


# Schema for registering a trip
class TripCreate(BaseModel):
    employee_id: str
    destination: str
    start_date: date
    end_date: date
    purpose: str


# Schema for asking a question
class ChatRequest(BaseModel):
    trip_id: int
    session_id: str
    question: str

class DashboardSummary(BaseModel):
    total: int
    by_status: dict[str, int]
    by_priority: dict[str, int]