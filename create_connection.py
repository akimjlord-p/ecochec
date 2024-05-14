import sqlite3
if __name__ == "create_connection":
    conn = sqlite3.connect('../db.db', check_same_thread=False)
    cursor = conn.cursor()

