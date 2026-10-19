from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    price: float
    stock: int

def get_connection():
    conn=psycopg2.connect(
        host="localhost",
        database="library_store",
        user="postgres",
        password="Admin@123")
    print("Connected to PostgreSQL successfully")
    return conn

@app.get("/books")
def get_books():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


