from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()

# Đường dẫn database (Render vẫn chạy được)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def read_root():
    return {"message": "Backend + Database hoạt động OK"}


@app.get("/users")
def get_users():
    conn = get_db()
    cursor = conn.cursor()

    # Tạo bảng nếu chưa tồn tại
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    # Chỉ insert nếu bảng đang rỗng
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Test User",))
        conn.commit()

    users = cursor.execute("SELECT * FROM users").fetchall()
    conn.close()

    # Trả dữ liệu dạng JSON
    return [dict(user) for user in users]
