import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="coworking_demo",
    user="postgres",
    password="Admin@123",
    port="5432"
)

cursor = conn.cursor()

print("Connected to PostgreSQL")


# cursor.execute("""
# CREATE TABLE IF NOT EXISTS rooms (
#     room_id SERIAL PRIMARY KEY,
#     room_name VARCHAR(100),
#     capacity INT,
#     hourly_rate FLOAT,
#     status VARCHAR(100)
# )
# """)
#
# conn.commit()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS bookings (
#     booking_id SERIAL PRIMARY KEY,
#     room_id INT,
#     booked_by VARCHAR(100),
#
#     booking_date DATE,
#     hours INT,
#     FOREIGN KEY(room_id) REFERENCES rooms(room_id)
# )
# """)
#
# conn.commit()
#
# print("Tables created successfully!")

# cursor.execute("""
# INSERT INTO rooms
# (room_id, room_name, capacity, hourly_rate, status)
# VALUES
# (101, 'Focus Room', 5, 2000.00,'Available'),
# (102, 'Conference Room', 50, 15000.00,'Maintainence'),
# (103, 'Creative Studio', 10, 7000.00,'Available'),
# (104, 'Board Room', 20, 5000.00,'Available')
# """)
#
# conn.commit()
#
# print("Records inserted for rooms")

# cursor.execute("""
# INSERT INTO bookings
# (booking_id,room_id,booked_by,booking_date, hours)
# VALUES
# (1001,101,'Anna','2026-01-10',24),
# (1002,101,'Agnus','2026-01-12',48),
# (1003,103,'Maheep','2026-01-10',10),
# (1004,104,'Jay','2026-01-15',24),
# (1005,102,'Thomas','2026-01-11',48),
# (1006,101,'Mariya','2026-01-13',72)
#
#
# """)
#
# conn.commit()
#
# print("Records inserted for bookings")


# cursor.execute("SELECT * FROM rooms")
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)

# cursor.execute("SELECT * FROM bookings")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.execute("""SELECT * FROM rooms WHERE capacity>6""")
# rows=cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.execute("""SELECT * FROM rooms WHERE
# status='Available'
# """)
# for row in cursor.fetchall():
#     print(row)

# cursor.execute("""SELECT * FROM bookings WHERE
# booked_by='Anna'
# """)
# for row in cursor.fetchall():
#     print(row)

# cursor.execute("""
# UPDATE rooms SET hourly_rate=40.00 WHERE room_id=103
# """)
# conn.commit()
# cursor.execute("""SELECT * FROM rooms""")
#
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)

# cursor.execute(""" UPDATE rooms set Status='Maintainence' WHERE room_id=101""")
# conn.commit()
# cursor.execute("SELECT * FROM rooms")
# rows=cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.execute(""" UPDATE bookings SET hours=8 WHERE booking_id=1001""")
# conn.commit()
# cursor.execute("SELECT * FROM bookings")
# rows=cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.execute("""
# DELETE FROM bookings
# WHERE booking_id = 1002
# """)
#
# conn.commit()
# cursor.execute("SELECT * FROM bookings")
# rows=cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.execute('''SELECT b.booking_id,b.booked_by,r.room_name,b.booking_date,b.hours,r.hourly_rate
# FROM rooms r
# JOIN bookings b
# ON r.room_id=b.room_id
# ''')
# rows=cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.execute('''SELECT r.room_name,count(b.booking_id)
# FROM rooms r
# JOIN bookings b
# ON b.room_id = r.room_id
# GROUP BY r.room_name''')
# rows=cursor.fetchall()
# for row in rows:
#      print(row)

# cursor.execute('''SELECT MAX(hourly_rate) FROM rooms''')
# rows=cursor.fetchall()
# for row in rows:
#      print(row)

cursor.execute('''SELECT b.booked_by,r.room_name,b.hours,
b.hours* r.hourly_rate AS cost  
FROM rooms r
JOIN bookings b
ON r.room_id=b.room_id''')
rows=cursor.fetchall()
for row in rows:
     print(row)



