import bcrypt
from pathlib import Path
import sqlite3
import pandas as pd
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table, create_all_tables

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Validate input
    if not username or not password:
        return False, "Username and password are required."
    
    # Check if username already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return False, f"Username '{username}' already exists."
    
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        role = user[3]  # role column
        return True, f"Login successful! Welcome {username} (role: {role})."
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    path = Path(filepath)
    
    if not path.exists():
        print(f"Warning: {filepath} not found. Skipping migration.")
        return 0
    
    conn = connect_database()
    create_users_table(conn)
    cursor = conn.cursor()
    migrated_count = 0
    
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue
            
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                continue
            
            username = parts[0]
            password_hash = parts[1]
            role = parts[2] if len(parts) >= 3 else "user"
            
            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
                migrated_count += 1
            except sqlite3.IntegrityError:
                print(f"User '{username}' already exists. Skipping.")
    
    conn.commit()
    conn.close()
    return migrated_count

def load_all_csv_data():
    """Load all three domain CSV files into the database."""
    conn = connect_database()
    create_all_tables(conn)  # Ensure tables exist
    
    print("\nStarting CSV data loading...")
    total_rows = 0
    
    # Load cyber incidents
    cyber_path = Path("DATA/cyber_incidents.csv")
    if cyber_path.exists():
        df_cyber = pd.read_csv(cyber_path)
        print(f"Read {len(df_cyber)} rows from cyber_incidents.csv")
        print(f"   Columns found: {df_cyber.columns.tolist()}")
        
        # Clean column names
        df_cyber.columns = df_cyber.columns.str.strip()
        
        # Select only columns that match database schema
        required_cols = ['title', 'severity', 'status', 'date']
        
        # Check if we have required columns
        missing_cols = [col for col in required_cols if col not in df_cyber.columns]
        if missing_cols:
            print(f"   Warning: Missing columns: {missing_cols}")
            print(f"   Available columns: {df_cyber.columns.tolist()}")
        else:
            # Select only the required columns
            df_cyber = df_cyber[required_cols]
            # Load into database
            df_cyber.to_sql('cyber_incidents', conn, if_exists='append', index=False)
            print(f"   Loaded {len(df_cyber)} rows into 'cyber_incidents' table")
            total_rows += len(df_cyber)
    else:
        print("cyber_incidents.csv not found")
    
    # Load datasets metadata
    datasets_path = Path("DATA/datasets_metadata.csv")
    if datasets_path.exists():
        df_datasets = pd.read_csv(datasets_path)
        print(f"\nRead {len(df_datasets)} rows from datasets_metadata.csv")
        print(f"   Columns found: {df_datasets.columns.tolist()}")
        
        # Clean column names
        df_datasets.columns = df_datasets.columns.str.strip()
        
        # Select only columns that match database schema
        required_cols = ['name', 'source', 'category', 'size']
        
        # Check if we have required columns
        missing_cols = [col for col in required_cols if col not in df_datasets.columns]
        if missing_cols:
            print(f"   Warning: Missing columns: {missing_cols}")
            print(f"   Available columns: {df_datasets.columns.tolist()}")
        else:
            # Select only the required columns
            df_datasets = df_datasets[required_cols]
            # Load into database
            df_datasets.to_sql('datasets_metadata', conn, if_exists='append', index=False)
            print(f"   Loaded {len(df_datasets)} rows into 'datasets_metadata' table")
            total_rows += len(df_datasets)
    else:
        print("datasets_metadata.csv not found")
    
    # Load IT tickets
    tickets_path = Path("DATA/it_tickets.csv")
    if tickets_path.exists():
        df_tickets = pd.read_csv(tickets_path)
        print(f"\nRead {len(df_tickets)} rows from it_tickets.csv")
        print(f"   Columns found: {df_tickets.columns.tolist()}")
        
        # Clean column names
        df_tickets.columns = df_tickets.columns.str.strip()
        
        # Select only columns that match database schema
        required_cols = ['title', 'priority', 'status', 'created_date']
        
        # Check if we have required columns
        missing_cols = [col for col in required_cols if col not in df_tickets.columns]
        if missing_cols:
            print(f"   Warning: Missing columns: {missing_cols}")
            print(f"   Available columns: {df_tickets.columns.tolist()}")
        else:
            # Select only the required columns
            df_tickets = df_tickets[required_cols]
            # Load into database
            df_tickets.to_sql('it_tickets', conn, if_exists='append', index=False)
            print(f"   Loaded {len(df_tickets)} rows into 'it_tickets' table")
            total_rows += len(df_tickets)
    else:
        print("it_tickets.csv not found")
    
    conn.close()
    print(f"\nTotal rows loaded: {total_rows}")
    return total_rows