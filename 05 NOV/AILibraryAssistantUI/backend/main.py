
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from tools import (
    search_books_data,
    create_reservation,
    get_reservations
)


# =====================================================
# SECTION 1: CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="AI Library Assistant API",
    description="Backend for the React Library Assistant",
    version="1.0"
)


# =====================================================
# SECTION 2: ENABLE REACT FRONTEND ACCESS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================================
# SECTION 3: RESERVATION REQUEST MODEL
# =====================================================

class ReservationRequest(BaseModel):

    book_id: int

    customer_name: str


# =====================================================
# SECTION 4: GET AND SEARCH BOOKS
# =====================================================

@app.get("/api/books")
def get_books(search: str = ""):

    return search_books_data(search)


# =====================================================
# SECTION 5: CREATE A RESERVATION
# =====================================================

@app.post("/api/reservations")
def reserve_a_book(request: ReservationRequest):

    result = create_reservation(
        book_id=request.book_id,
        customer_name=request.customer_name
    )

    if not result["success"]:

        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


# =====================================================
# SECTION 6: GET ALL RESERVATIONS
# =====================================================

@app.get("/api/reservations")
def get_all_reservations():

    return get_reservations()


# =====================================================
# SECTION 7: HEALTH CHECK
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Library Assistant API is running!"
    }
