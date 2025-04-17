import sqlite3

# SQL query to insert data into the project table
data_insert_query = """
INSERT INTO project (age, flight_distance, inflight_entertainment, baggage_handling, cleanliness, 
                    departure_delay, arrival_delay, gender, customer_type, travel_type, 
                    class_type, prediction)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

def create_table():
    """
    Function to create the project table if it does not exist
    """
    conn = sqlite3.connect('customer_satisfaction.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS project (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        flight_distance INTEGER,
        inflight_entertainment INTEGER,
        baggage_handling INTEGER,
        cleanliness INTEGER,
        departure_delay INTEGER,
        arrival_delay INTEGER,
        gender INTEGER,
        customer_type INTEGER,
        travel_type INTEGER,
        class_type TEXT,
        prediction TEXT
    )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_data(data):
    """
    Function to insert data into the project table
    """
    conn = sqlite3.connect('customer_satisfaction.db')
    cur = conn.cursor()
    cur.execute(data_insert_query, data)
    conn.commit()
    cur.close()
    conn.close()