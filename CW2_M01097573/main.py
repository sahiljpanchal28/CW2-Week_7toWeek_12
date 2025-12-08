import os
import sys
from pathlib import Path
import pandas as pd
import sqlite3

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.data.db import connect_database
from app.data.schema import (
    create_users_table,
    create_cyber_incidents_table,
    create_datasets_metadata_table,
    create_it_tickets_table
)
from app.data.incidents import insert_incident, get_all_incidents
from app.data.tickets import insert_ticket, get_all_tickets
from app.data.datasets import insert_dataset, get_all_datasets
from app.data.users import insert_user, get_all_users


def clear_tables():
    """Clear all tables without dropping them"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM cyber_incidents")
        cursor.execute("DELETE FROM it_tickets")
        cursor.execute("DELETE FROM datasets_metadata")
        cursor.execute("DELETE FROM sqlite_sequence")
        conn.commit()
        print("[OK] All tables cleared")
    except Exception as e:
        print(f"[WARNING] {e}")
    finally:
        conn.close()


def load_csv_data():
    """Load CSV data into the database"""
    # Get absolute path to DATA directory
    data_dir = Path(__file__).parent / "DATA"
    
    # Load users - skip comment line, manually set column names
    try:
        users_path = data_dir / 'users.txt'
        users_df = pd.read_csv(users_path, comment='#', header=None, names=['username', 'password_hash', 'role'])
        for _, row in users_df.iterrows():
            insert_user(row['username'], row['password_hash'], row['role'])
        print(f"[OK] Loaded {len(users_df)} users")
    except Exception as e:
        print(f"[WARNING] Users: {e}")
    
    # Load cyber incidents - select only matching columns
    try:
        incidents_path = data_dir / 'cyber_incidents.csv'
        incidents_df = pd.read_csv(incidents_path)
        # Select only columns that match database schema
        incidents_df = incidents_df[['title', 'severity', 'status', 'date']]
        for _, row in incidents_df.iterrows():
            insert_incident(
                title=row['title'],
                severity=row['severity'],
                status=row['status'],
                date=row['date']
            )
        print(f"[OK] Loaded {len(incidents_df)} cyber incidents")
    except Exception as e:
        print(f"[WARNING] Incidents: {e}")
    
    # Load IT tickets - select only matching columns
    try:
        tickets_path = data_dir / 'it_tickets.csv'
        tickets_df = pd.read_csv(tickets_path)
        # Select only columns that match database schema
        tickets_df = tickets_df[['title', 'priority', 'status', 'created_date']]
        for _, row in tickets_df.iterrows():
            insert_ticket(
                title=row['title'],
                priority=row['priority'],
                status=row['status'],
                created_date=row['created_date']
            )
        print(f"[OK] Loaded {len(tickets_df)} IT tickets")
    except Exception as e:
        print(f"[WARNING] Tickets: {e}")
    
    # Load datasets - select only matching columns
    try:
        datasets_path = data_dir / 'datasets_metadata.csv'
        datasets_df = pd.read_csv(datasets_path)
        # Select only columns that match database schema
        datasets_df = datasets_df[['name', 'source', 'category', 'size']]
        for _, row in datasets_df.iterrows():
            insert_dataset(
                name=row['name'],
                source=row['source'],
                category=row['category'],
                size=row['size']
            )
        print(f"[OK] Loaded {len(datasets_df)} datasets")
    except Exception as e:
        print(f"[WARNING] Datasets: {e}")


def test_authentication():
    """Test user registration"""
    print("Testing user creation...")
    try:
        insert_user("testuser_new", "hashed_test_pass_123", "analyst")
        print(f"[OK] User 'testuser_new' created successfully")
    except Exception as e:
        print(f"[WARNING] Auth test: {e}")


def test_crud():
    """Test CRUD operations"""
    # Test incidents
    try:
        incident_id = insert_incident(
            title="Phishing Attack Detected",
            severity="High",
            status="open",
            date="2024-11-05"
        )
        print(f"[OK] Created incident #{incident_id}")
        df = get_all_incidents()
        print(f"[OK] Total incidents: {len(df)}")
    except Exception as e:
        print(f"[WARNING] Incident CRUD: {e}")
    
    # Test tickets
    try:
        ticket_id = insert_ticket(
            title="Cannot access VPN",
            priority="High",
            status="open",
            created_date="2024-11-05"
        )   
        print(f"[OK] Created ticket #{ticket_id}")
        df_tickets = get_all_tickets()
        print(f"[OK] Total tickets: {len(df_tickets)}")
    except Exception as e:
        print(f"[WARNING] Ticket CRUD: {e}")
    
    # Test datasets
    try:
        dataset_id = insert_dataset(
            name="Employee Data",
            source="HR System",
            category="Internal",
            size=2048
        )
        print(f"[OK] Created dataset #{dataset_id}")
        df_datasets = get_all_datasets()
        print(f"[OK] Total datasets: {len(df_datasets)}")
    except Exception as e:
        print(f"[WARNING] Dataset CRUD: {e}")
    
    # Test users
    try:
        insert_user(
            username="newuser_test",
            password_hash="hashed_password_123",
            role="admin"
        )
        users = get_all_users()
        print(f"[OK] Total users in database: {len(users)}")
    except Exception as e:
        print(f"[WARNING] User CRUD: {e}")


def query_and_display_tables():
    """Query and display all four tables"""
    print("\n" + "=" * 60)
    print("FOUR TABLE SUMMARY")
    print("=" * 60)
    
    # Query incidents
    try:
        df_incidents = get_all_incidents()
        print(f"\nTABLE 1: CYBER INCIDENTS ({len(df_incidents)} records)")
        if len(df_incidents) > 0:
            print(df_incidents.head(3).to_string())
        else:
            print("No records")
    except Exception as e:
        print(f"[WARNING] Incidents table: {e}")
    
    # Query tickets
    try:
        df_tickets = get_all_tickets()
        print(f"\nTABLE 2: IT TICKETS ({len(df_tickets)} records)")
        if len(df_tickets) > 0:
            print(df_tickets.head(3).to_string())
        else:
            print("No records")
    except Exception as e:
        print(f"[WARNING] Tickets table: {e}")
    
    # Query datasets
    try:
        df_datasets = get_all_datasets()
        print(f"\nTABLE 3: DATASETS METADATA ({len(df_datasets)} records)")
        if len(df_datasets) > 0:
            print(df_datasets.head(3).to_string())
        else:
            print("No records")
    except Exception as e:
        print(f"[WARNING] Datasets table: {e}")
    
    # Query users
    try:
        users = get_all_users()
        df_users = pd.DataFrame(users, columns=['ID', 'Username', 'Role'])
        print(f"\nTABLE 4: USERS ({len(users)} records)")
        if len(users) > 0:
            print(df_users.head(3).to_string())
        else:
            print("No records")
    except Exception as e:
        print(f"[WARNING] Users table: {e}")


def main():
    print("=" * 60)
    print("WEEK 8: DATABASE SETUP & DEMO")
    print("=" * 60)

    print("\n[1/6] Setting up database...")
    try:
        conn = connect_database()
        create_users_table(conn)
        create_cyber_incidents_table(conn)
        create_datasets_metadata_table(conn)
        create_it_tickets_table(conn)
        conn.close()
        print("[OK] Database setup complete")
    except Exception as e:
        print(f"[WARNING] Database setup: {e}")
        return
    
    print("\n[2/6] Clearing previous data...")
    clear_tables()
    
    print("\n[3/6] Loading CSV data...")
    load_csv_data()
    
    print("\n[4/6] Testing user creation...")
    test_authentication()
    
    print("\n[5/6] Testing CRUD operations...")
    test_crud()
    
    print("\n[6/6] Displaying four tables...")
    query_and_display_tables()
    
    print("\n" + "=" * 60)
    print("[OK] Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()