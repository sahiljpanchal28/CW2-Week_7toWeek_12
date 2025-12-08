import pandas as pd
from app.data.db import connect_database

def insert_ticket(title, priority, status="open", created_date=None):
    """Insert new IT ticket."""
    conn = connect_database()
    cursor = conn.cursor()
    
    if created_date is None:
        from datetime import datetime
        created_date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute("""
        INSERT INTO it_tickets 
        (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
    """, (title, priority, status, created_date))
    
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

def get_all_tickets():
    """Get all IT tickets."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df

def get_tickets_by_status(status):
    """Get tickets by status."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets WHERE status = ?",
        conn,
        params=(status,)
    )
    conn.close()
    return df