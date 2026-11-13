
from database import get_db_connection
from security import hash_password


# Sample login credentials
users = [
    {
        "username": "arun",
        "password": "Arun@123"
    },
    {
        "username": "priya",
        "password": "Priya@123"
    }
]


connection = get_db_connection()

try:
    cursor = connection.cursor()

    for user in users:

        # Generate secure password hash
        hashed_password = hash_password(user["password"])

        # Update the password hash in PostgreSQL
        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s
            WHERE username = %s;
            """,
            (hashed_password, user["username"])
        )

        print(f"Password updated for {user['username']}")

    connection.commit()

    print("All user passwords updated successfully!")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()
