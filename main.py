from key_manager import KeyManager
from encryption_handler import EncryptionHandler
from database_manager import DatabaseManager
from password_manager import PasswordManager
import getpass

def first_time_setup(key_manager, db_manager):
    print("Welcome! It looks like this is your first time using the program.")

    master_password = getpass.getpass("Please set your master password: ")
    confirm_password = getpass.getpass("Enter again to confirm: ")

    if master_password == confirm_password:
        key = key_manager.derive_key(master_password)
        encryption_handler = EncryptionHandler(key)
        master_hash = encryption_handler.hash_master_password(master_password)
        db_manager.store_master_hash(master_hash)
        print("Master password set successfully!")
    else:
        print("Passwords do not match. Please try again.")
        first_time_setup()

def main():
    key_manager = KeyManager()
    db_manager = DatabaseManager()
    encryption_handler = None
    password_manager = None

    master_hash = db_manager.get_master_hash()

    if master_hash == None:
        first_time_setup(key_manager, db_manager)
        password_manager = PasswordManager(db_manager, encryption_handler)
        password_manager.authenticate_user(master_password)
    else:
        master_password = getpass.getpass("Enter master password: ")
        key = key_manager.derive_key(master_password)
        encryption_handler = EncryptionHandler(key)
        password_manager = PasswordManager(db_manager, encryption_handler)
        password_manager.authenticate_user(master_password)
    
    while True:
        print("\nPassword Manager Menu:")
        print("1. Add new service password")
        print("2. Retrieve a password")
        print("3. Update a password")
        print("4. Delete a password")
        print("5. List all stored services")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            password_manager.add_service()
        elif choice == '2':
            password_manager.get_password()
        elif choice == '3':
            password_manager.update_password()
        elif choice == '4':
            password_manager.delete_password()
        elif choice == '5':
            password_manager.list_services()
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
if __name__ == '__main__':
    main()