
import psycopg2

def get_connection():

    conn = psycopg2.connect(
        host="localhost",
        database="travel_weather_db",
        user="postgres",
        password="Admin@123"
    )

    return conn


def create_trips_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (

        trip_id SERIAL PRIMARY KEY,

        employee_id VARCHAR(50),

        destination VARCHAR(100),

        start_date DATE,

        end_date DATE,

        purpose VARCHAR(200),

        status VARCHAR(30) DEFAULT 'Registered'

    )
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print("Trips table created successfully!")


if __name__ == "__main__":
    create_trips_table()
