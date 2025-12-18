from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

@app.get("/")
def read_root():
    return {"message": "Backend + Database hoạt động OK"}

@app.get("/users")
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES ('Test User')")
    conn.commit()
    users = cursor.execute("SELECT * FROM users").fetchall()
    conn.close()
    return users
