
import json
import uuid
from pathlib import Path

from langchain.tools import tool


# =====================================================
# SECTION 1: JSON FILE LOCATIONS
# =====================================================

ROOT = Path(__file__).resolve().parent

BOOKS_FILE = ROOT / "books.json"
RESERVATIONS_FILE = ROOT / "reservations.json"


# =====================================================
# SECTION 2: READ JSON FILES
# =====================================================

def get_books():

    return json.loads(
        BOOKS_FILE.read_text(encoding="utf-8")
    )


def get_reservations():

    return json.loads(
        RESERVATIONS_FILE.read_text(encoding="utf-8")
    )


# =====================================================
# SECTION 3: SAVE JSON FILES
# =====================================================

def save_books(books):

    BOOKS_FILE.write_text(
        json.dumps(books, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def save_reservations(reservations):

    RESERVATIONS_FILE.write_text(
        json.dumps(reservations, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


# =====================================================
# SECTION 4: SEARCH BOOKS
# =====================================================

def search_books_data(keyword=""):

    books = get_books()

    keyword = keyword.strip().lower()

    if not keyword:
        return books

    matching_books = []

    for book in books:

        if (
            keyword in book["title"].lower()
            or keyword in book["author"].lower()
            or keyword in book["category"].lower()
        ):

            matching_books.append(book)

    return matching_books


# =====================================================
# SECTION 5: CREATE RESERVATION
# =====================================================

def create_reservation(book_id: int, customer_name: str):

    books = get_books()

    reservations = get_reservations()

    for book in books:

        if book["id"] == book_id:

            if book["available_copies"] <= 0:

                return {
                    "success": False,
                    "message": "Book is not available."
                }

            if not customer_name.strip():

                return {
                    "success": False,
                    "message": "Customer name is required."
                }

            reservation = {

                "reservation_id": "RES-" + uuid.uuid4().hex[:8].upper(),

                "book_id": book["id"],

                "customer_name": customer_name.strip(),

                "title": book["title"],

                "author": book["author"]

            }

            # Reduce available copies
            book["available_copies"] -= 1

            # Add reservation
            reservations.append(reservation)

            # Save both JSON files
            save_books(books)

            save_reservations(reservations)

            return {
                "success": True,
                "message": "Book reserved successfully!",
                "reservation": reservation
            }

    return {
        "success": False,
        "message": "Book ID not found."
    }


# =====================================================
# SECTION 6: LANGCHAIN TOOL 1
# =====================================================

@tool
def search_book(keyword: str) -> str:
    """Search books by title, author, or category."""

    result = search_books_data(keyword)

    return json.dumps(result, ensure_ascii=False)


# =====================================================
# SECTION 7: LANGCHAIN TOOL 2
# =====================================================

@tool
def reserve_book(book_id: int, cust_name: str) -> str:
    """Reserve an available book for a customer."""

    result = create_reservation(
        book_id=book_id,
        customer_name=cust_name
    )

    return json.dumps(result, ensure_ascii=False)
