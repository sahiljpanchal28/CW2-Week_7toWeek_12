import pandas as pd
from app.data.db import connect_database

def insert_dataset(name, source, category, size):
    """Insert new dataset metadata."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (name, source, category, size)
        VALUES (?, ?, ?, ?)
    """, (name, source, category, size))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

def get_all_datasets():
    """Get all datasets metadata."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df

def get_datasets_by_category(category):
    """Get datasets by category."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata WHERE category = ?",
        conn,
        params=(category,)
    )
    conn.close()
    return df