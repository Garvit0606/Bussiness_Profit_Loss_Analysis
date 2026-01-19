import sqlite3
from datetime import datetime, timedelta
from database import get_connection

def signup(email, password):
    conn = get_connection()
    cur = conn.cursor()

    expiry = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

    cur.execute("""
        INSERT OR IGNORE INTO users (email, password, plan, expiry)
        VALUES (?, ?, ?, ?)
    """, (email, password, "FREE", expiry))

    conn.commit()
    conn.close()

def login(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT email, password, plan, expiry
        FROM users
        WHERE email=? AND password=?
    """, (email, password))

    user = cur.fetchone()
    conn.close()

    return user

