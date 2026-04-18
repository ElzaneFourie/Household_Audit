import sqlite3, os

def initialise_database():
    conn = sqlite3.connect("data/household.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS household_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        folder_name TEXT
        )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS statements (
        statement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        month TEXT,
        FOREIGN KEY (member_id) REFERENCES household_members(id)
        )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
        transactions_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        statement_id INTEGER,
        category TEXT,
        description TEXT,
        transaction_date TEXT,
        amount REAL,
        FOREIGN KEY (member_id) REFERENCES household_members(id),
        FOREIGN KEY (statement_id) REFERENCES statements(statements_id)
        )""")
    conn.commit()
    conn.close()
    
def add_member(member_name):
    folder_name = member_name.lower().replace(" ", "_")
    conn = sqlite3.connect("data/household.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO household_members (name, folder_name) VALUES (?,?)""", (member_name, folder_name))
    conn.commit()
    conn.close()
    os.makedirs(f"data/statements/{folder_name}", exist_ok = True)

def get_members():
    conn = sqlite3.connect("data/household.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM household_members""")
    conn.close()
    return cursor.fetchall()