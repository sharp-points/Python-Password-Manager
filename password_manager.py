import db
import getpass
import encryption
import bcrypt

def first_time_setup():
    print("Welcome! It looks like this is your first time using the program.")

    master_password = getpass.getpass("Please set your master password.")
    confirm_password = getpass.getpass("Enter again to confirm.")

    if master_password == confirm_password:
        master_hash = encryption.hash_master_password(master_password)
        db.store_master_password_hash(master_hash)
    else:
        print("Passwords do not match. Try again.")
        first_time_setup()


def authenticate_user():
    # Fetch stored hash for master password
    stored_tuple = db.get_master_password_hash()

    stored_hash = stored_tuple[0]

    # Ask the user for the master password
    entered_password = getpass.getpass("Enter Master Password: ")

    result = bcrypt.checkpw(entered_password.encode(), stored_hash)

    if result:
        print("Authentication successful.")
        return True
    else:
        print("Authentication failed.")
        return False

def add_new_service():
    service_url = input("Enter website URL: ")
    username = input("Enter username/email: ")
    raw_password = getpass.getpass("Enter password: ")

    aes_key = encryption.decrypt_aes_key()

    encrypted_password = encryption.encrypt_password(aes_key, raw_password)

    encryption.remove_unencrypted_data()
    aes_key = None

    db.store_password(service_url, username, encrypted_password)
    print(f"Password for {service_url} stored.")

def get_password():
    service_url = input("Enter website URL to retrieve password for: ")
    username = input(f"Enter {service_url} username/email to retrieve password for: ")

    aes_key = encryption.decrypt_aes_key()

    encrypted_password = db.get_password(service_url, username)
    
    if encrypted_password:
        decrypted_password = encryption.decrypt_password(aes_key, encrypted_password)
        print(f"Password for {service_url} username {username}: {decrypted_password}")
    else:
        print(f"No password found for {service_url} username {username}")
        print("Make sure there are no typos in the URL or username and try again.")
    
    encryption.remove_unencrypted_data()
    aes_key = None

def delete_password():
    service_url = input("Enter website URL to delete password for: ")
    username = input(f"Enter {service_url} username/email to delete password for: ")

    db.delete_password(service_url, username)

def update_password():
    service_url = input("Enter website URL to update password for: ")
    username = input(f"Enter {service_url} username/email to update password for: ")
    password = getpass.getpass("Enter new password: ")

    db.update_password(service_url, username, password)

def list_services():
    """List all stored services and usernames."""
    stored_information = db.retrieve_stored_information()

    if stored_information:
        print("\nStored services and usernames:")
        for service_url, username in stored_information:
            print(f"Service: {service_url} | Username: {username}")
    else:
        print("No services stored.")