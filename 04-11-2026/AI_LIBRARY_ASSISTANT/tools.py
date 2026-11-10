
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

BOOKS_FILE = BASE_DIR / "books.json"
RESERVATIONS_FILE = BASE_DIR / "reservations.json"


def read_books():
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_books(query):
    books = read_books()

    matching_books = []

    for book in books:
        if query.lower() in book["title"].lower() or \
           query.lower() in book["author"].lower() or \
           query.lower() in book["category"].lower():

            matching_books.append(book)

    if matching_books:
        return matching_books

    return "No matching books found."

def reserve_book(book_id, customer_name):
    books = read_books()

    selected_book = None

    for book in books:
        if book["id"] == book_id:
            selected_book = book
            break

    if selected_book is None:
        return "Book not found."

    if selected_book["available_copies"] <= 0:
        return "Sorry, this book is not available."

    print(
        f"\nBook: {selected_book['title']}"
        f"\nCustomer: {customer_name}"
    )

    confirmation = input("Do you want to confirm the reservation? (yes/no): ")

    if confirmation.lower() != "yes":
        return "Reservation cancelled."

    reservation = {
        "book_id": book_id,
        "book_title": selected_book["title"],
        "customer_name": customer_name
    }

    if RESERVATIONS_FILE.exists():
        with open(RESERVATIONS_FILE, "r", encoding="utf-8") as file:
            reservations = json.load(file)
    else:
        reservations = []

    reservations.append(reservation)

    with open(RESERVATIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(reservations, file, indent=4)

    selected_book["available_copies"] -= 1

    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4)

    return reservation
