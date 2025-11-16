import bcrypt
import os
import time
import secrets

def verify_password(password: str) -> str:
    pass_bytes = password.encode('utf-8')   
    # Create a random salt for security
    salt_value = bcrypt.gensalt()
    #  Produce the bcrypt hash using passwor and salt
    final_hase = bcrypt.hashpw(pass_bytes, salt)
    return final_hase.decode('utf-8')
def verify_password(password: str, hashed: str) -> bool:
    pass_bytes = password.encode('utf-8')
    hash_bytes = hashed.encode('utf-8')
    # Verify the password against the hashed value
    x = bcrypt.checkpw(pass_bytes, hash_bytes)
    return x
'''
sample_password = "SecurePassword123"
hashed = hash_password(sample_password)
print(f"Original password: {sample_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")
# Test verification with correct password
is_valid = verify_password(sample_password, hashed)
print(f"\nVerification with correct password: {is_valid}")
# Test verification with incorrect password
check_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {check_invalid}")
'''
USER_DATA_FILE = 'user_data.txt'
def register_user(username: str, password: str) -> None:
    try:
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                existing_username = line.split(',')[0]
                if existing_username == username:
                    raise ValueError("Username already exists.")
    except FileNotFoundError:
        pass  # File does not exist yet, so no users are registered
    hashed_password = hashed_password(password)
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
        print(f"User '{username}' registered successfully.")    
    return True
def user_exists(username, filename='user_data.txt'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                existing_username, _ = line.strip().split(',', 1)
                if existing_username == username:
                    return True
    except FileNotFoundError:
        # File doesn't exist yet, so no users registered
        return False

    return False


def verify_password(plain_text_password, stored_hash):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), stored_hash.encode('utf-8'))

def login_user(username, password, filename='user_data.txt'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                stored_username, stored_hash = line.strip().split(',', 1)
                if stored_username == username:
                    if verify_password(password, stored_hash):
                        print(f"User '{username}' logged in successfully.")
                        return True
                    else:
                        print("Error: Incorrect password.")
                        return False
                else:
                    print("Error: Username not found.")
                    return False
    except FileNotFoundError:
        return False

    return False                 # If we reach here, the username was not found

def validate_username(username: str) -> bool:
    if not username:
        return (False, "Username cannot be empty.")
    
    if len(username) < 3:
        return (False, "Username must be at least 3 characters long.")
    
    if not username.isalnum():
        return (False, "Username must contain only letters and numbers.")

    return (True, "")

def validate_password(password: str) -> bool:
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long.")
    
    if not any(char.isdigit() for char in password):
        return (False, "Password must contain at least one number.")
    
    if not any(char.isupper() for char in password):
        return (False, "Password must contain at least one uppercase letter.")
    
    if not any(char.islower() for char in password):
        return (False, "Password must contain at least one lowercase letter.")
    
    return (True, "")

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            password = input("Enter a password: ").strip()
            # Validate password
            is_valid,error_msg = validate_password(password)
            if not is_valid:
                print(f"Error:{error_msg}")
                continue
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            # Register the user
            register_user(username, password)
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            # Attempt login
            if login_user(username,password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the data platform.)")
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()

#Extensions: Optional Tasks

#1. Password Strength Checker
def check_password_strength(password):
    # Criteria flags
    length_ok = len(password) >= 8
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password)

    # Common weak passwords
    comm_pass = {"password", "123456", "qwerty", "letmein", "admin", "welcome"}
    common = password.lower() in comm_pass

    # Strength scoring
    score = sum([length_ok, has_upper, has_lower, has_digit, has_special])
    if common:
        return "Very Weak"

    if score == 5:
        return "Strong"
    elif score >= 3:
        return "Moderate"
    else:
        return "Weak"

#2. User Role System
def register_user(username, password, role="user", filename='user_data.txt'):
    # Validate role
    valid_roles = {"user", "admin", "analyst"}
    if role not in valid_roles:
        print(f"Invalid role: '{role}'. Must be one of {valid_roles}.")
        return False

    # Check if username already exists
    try:
        with open(filename, 'r') as file:
            for line in file:
                existing_username = line.strip().split(',')[0]
                if existing_username == username:
                    print("Username already exists.")
                    return False
    except FileNotFoundError:
        pass  # No users registered yet

    # Hash the password
    hashed_password = hash_password(password)

    # Append user with role
    with open(filename, 'a') as file:
        file.write(f"{username},{hashed_password},{role}\n")
    print(f"User '{username}' with role '{role}' registered successfully.")

    return True

#3. Account Lockout Mechanism


def current_timestamp():
    return int(time.time())

def is_account_locked(username, filename='failed_attempts.txt'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                user, count, last_time = line.strip().split(',')
                if user == username:
                    count = int(count)
                    last_time = int(last_time)
                    if count >= 3 and current_timestamp() - last_time < 300:
                        return True
    except FileNotFoundError:
        pass
    return False

def update_failed_attempts(username, success, filename='failed_attempts.txt'):
    attempts = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                user, count, last_time = line.strip().split(',')
                attempts[user] = (int(count), int(last_time))
    except FileNotFoundError:
        pass

    if success:
        attempts.pop(username, None)
    else:
        count, _ = attempts.get(username, (0, 0))
        attempts[username] = (count + 1, current_timestamp())

    with open(filename, 'w') as file:
        for user, (count, last_time) in attempts.items():
            file.write(f"{user},{count},{last_time}\n")

def login_user(username, password, filename='user_data.txt'):
    if is_account_locked(username):
        print("Account is locked. Try again later.")
        return False

    try:
        with open(filename, 'r') as file:
            for line in file:
                stored_username, stored_hash = line.strip().split(',', 1)
                if stored_username == username:
                    if verify_password(password, stored_hash):
                        update_failed_attempts(username, success=True)
                        print(f"User '{username}' logged in successfully.")
                        return True
                    else:
                        print("Error: Incorrect password.")
                        return False
                else:
                    update_failed_attempts(username, success=False)
                    print("Error: Username not found.")
                    return False
    except FileNotFoundError:
        return False

    return False 

#4. Session Management



def current_timestamp():
    return int(time.time())

def create_session(username, filename='sessions.txt'):
    token = secrets.token_hex(16)
    timestamp = current_timestamp()

    # Store session as: username,token,timestamp
    with open(filename, 'a') as file:
        file.write(f"{username},{token},{timestamp}\n")

    return token

