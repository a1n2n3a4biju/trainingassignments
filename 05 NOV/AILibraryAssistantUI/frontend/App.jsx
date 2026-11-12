
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";


function App() {

    // ==========================================
    // SECTION 1: REACT STATE
    // ==========================================

    const [books, setBooks] = useState([]);

    const [reservations, setReservations] = useState([]);

    const [search, setSearch] = useState("");

    const [customerName, setCustomerName] = useState("");

    const [loading, setLoading] = useState(false);

    const [message, setMessage] = useState("");

    const [error, setError] = useState("");


    // ==========================================
    // SECTION 2: FETCH BOOKS FROM FASTAPI
    // ==========================================

    async function fetchBooks(keyword = "") {

        try {

            setLoading(true);

            const response = await fetch(
                `${API_URL}/api/books?search=${encodeURIComponent(keyword)}`
            );

            if (!response.ok) {
                throw new Error("Unable to fetch books");
            }

            const data = await response.json();

            setBooks(data);

        } catch (err) {

            setError(err.message);

        } finally {

            setLoading(false);

        }
    }


    // ==========================================
    // SECTION 3: FETCH RESERVATIONS
    // ==========================================

    async function fetchReservations() {

        try {

            const response = await fetch(
                `${API_URL}/api/reservations`
            );

            if (!response.ok) {
                throw new Error("Unable to fetch reservations");
            }

            const data = await response.json();

            setReservations(data);

        } catch (err) {

            setError(err.message);

        }
    }


    // ==========================================
    // SECTION 4: LOAD DATA WHEN PAGE OPENS
    // ==========================================

    useEffect(() => {

        fetchBooks(search);

    }, [search]);


    useEffect(() => {

        fetchReservations();

    }, []);


    // ==========================================
    // SECTION 5: RESERVE A BOOK
    // ==========================================

    async function reserveBook(bookId) {

        setMessage("");
        setError("");

        if (!customerName.trim()) {

            setError("Please enter your name before reserving.");

            return;
        }


        const confirmed = window.confirm(
            "Are you sure you want to reserve this book?"
        );

        if (!confirmed) {
            return;
        }


        try {

            const response = await fetch(
                `${API_URL}/api/reservations`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        book_id: bookId,
                        customer_name: customerName
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail || "Reservation failed"
                );

            }


            setMessage(
                data.message
            );

            // Refresh available books
            await fetchBooks(search);

            // Refresh reservation list
            await fetchReservations();

        } catch (err) {

            setError(err.message);

        }
    }


    // ==========================================
    // SECTION 6: DISPLAY THE USER INTERFACE
    // ==========================================

    return (

        <div className="app-container">

            <header className="header">

                <div>
                    <h1>LibraAI</h1>

                    <p>AI Library Assistant</p>
                </div>

            </header>


            <main className="main-content">


                {/* SEARCH SECTION */}

                <section className="search-section">

                    <h2>Find Your Book</h2>

                    <input
                        type="text"
                        placeholder="Search by title, author, or category..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />

                    <input
                        type="text"
                        placeholder="Enter customer name"
                        value={customerName}
                        onChange={(e) => setCustomerName(e.target.value)}
                    />

                </section>


                {/* SUCCESS MESSAGE */}

                {message && (

                    <div className="success-message">
                        {message}
                    </div>

                )}


                {/* ERROR MESSAGE */}

                {error && (

                    <div className="error-message">
                        {error}
                    </div>

                )}


                {/* BOOKS SECTION */}

                <section className="books-section">

                    <h2>Available Books</h2>


                    {loading ? (

                        <p>Loading books...</p>

                    ) : books.length === 0 ? (

                        <p>No matching books found.</p>

                    ) : (

                        <div className="book-grid">

                            {books.map((book) => (

                                <div
                                    className="book-card"
                                    key={book.id}
                                >

                                    <div className="book-icon">
                                        📚
                                    </div>


                                    <h3>{book.title}</h3>

                                    <p>
                                        <strong>Author:</strong> {book.author}
                                    </p>

                                    <p>
                                        <strong>Category:</strong> {book.category}
                                    </p>

                                    <p>
                                        <strong>Book ID:</strong> {book.id}
                                    </p>


                                    <p className={
                                        book.available_copies > 0
                                            ? "available"
                                            : "unavailable"
                                    }>

                                        {book.available_copies > 0

                                            ? `${book.available_copies} copies available`

                                            : "Out of stock"

                                        }

                                    </p>


                                    <button
                                        onClick={() => reserveBook(book.id)}
                                        disabled={book.available_copies <= 0}
                                    >

                                        Reserve Book

                                    </button>

                                </div>

                            ))}

                        </div>

                    )}

                </section>


                {/* RESERVATIONS SECTION */}

                <section className="reservations-section">

                    <h2>My Reservations</h2>


                    {reservations.length === 0 ? (

                        <p>No reservations yet.</p>

                    ) : (

                        <div className="reservation-list">

                            {reservations.map((reservation) => (

                                <div
                                    className="reservation-card"
                                    key={reservation.reservation_id}
                                >

                                    <h3>{reservation.title}</h3>

                                    <p>
                                        <strong>Reservation ID:</strong>{" "}
                                        {reservation.reservation_id}
                                    </p>

                                    <p>
                                        <strong>Book ID:</strong>{" "}
                                        {reservation.book_id}
                                    </p>

                                    <p>
                                        <strong>Author:</strong>{" "}
                                        {reservation.author}
                                    </p>

                                    <p>
                                        <strong>Customer:</strong>{" "}
                                        {reservation.customer_name}
                                    </p>

                                    <span className="reserved-badge">
                                        Reserved
                                    </span>

                                </div>

                            ))}

                        </div>

                    )}

                </section>

            </main>

        </div>

    );

}

export default App;
