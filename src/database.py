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

def save_statement(member_id, month):
    conn = sqlite3.connect("data/household.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO statements (member_id, month) VALUES (?,?)""", (member_id, month))
    conn.commit()
    statement_id = cursor.lastrowid
    conn.close()
    return statement_id

def save_transaction(member_id, statement_id, category, description, transaction_date, amount):
    conn = sqlite3.connect("data/household.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO transactions (member_id, statement_id, category, description, transaction_date, amount)
                   VALUES (?,?,?,?,?,?)""", (member_id, statement_id, category, description, transaction_date, amount))
    conn.commit()
    conn.close()
    
def get_transactions(member_id=None, month=None):
    conn = sqlite3.connect("data/household.db")
    cursor = conn.cursor()
    
    query = """SELECT transactions.*
            FROM transactions
            JOIN statements ON transactions.statement_id = statements.statement_id"""
    conditions = []
    values = []
    
    if member_id is not None:
        conditions.append("transactions.member_id = ?")
        values.append(member_id)
        
    if month is not None:
        conditions.append("statements.month = ?")
        values.append(month)
        
    if conditions: query += " WHERE " + " AND ".join(conditions)
    
    cursor.execute(query, values)
    results = cursor.fetchall()
    conn.close()
    
    return results