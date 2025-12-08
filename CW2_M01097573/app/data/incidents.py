import pandas as pd
from app.data.db import connect_database

def insert_incident(title, severity, status="open", date=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    
    if date is None:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (title, severity, status, date)
        VALUES (?, ?, ?, ?)
    """, (title, severity, status, date))
    
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def get_incidents_by_severity(severity):
    """Get incidents by severity."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE severity = ?",
        conn,
        params=(severity,)
    )
    conn.close()
    return df

def update_incident_status(incident_id, new_status):
    """Update incident status."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0