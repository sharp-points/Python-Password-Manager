import getpass
import bcrypt


class PasswordManager:
    def __init__(self, db_manager, encryption_handler):
        self.db_manager = db_manager
        self.encryption_handler = encryption_handler

    def first_time_setup(self):
        print("Welcome! It looks like this is your first time using the program.")

        master_password = getpass.getpass("Please set your master password: ")
        confirm_password = getpass.getpass("Enter again to confirm: ")

        if master_password == confirm_password:
            master_hash = self.encryption_handler.hash_master_password(master_password)
            self.db_manager.store_master_hash(master_hash)
            print("Master password set successfully!")
        else:
            print("Passwords do not match. Please try again.")
            self.first_time_setup()
    
    def authenticate_user(self, entered_password):
        stored_tuple = self.db_manager.get_master_hash()

        if not stored_tuple:
            print("No master password set.")
            return False
        
        stored_hash = stored_tuple[0]

        if bcrypt.checkpw(entered_password.encode(), stored_hash):
            print("Authentication successful.")
            return True
        else:
            print("Authentication failed.")
            return False
        
    def add_service(self):
        service = input("Enter service URL or name: ")
        username = input("Enter username or email: ")
        raw_password = getpass.getpass("Enter password: ")

        encrypted_password = self.encryption_handler.encrypt(raw_password)

        self.db_manager.store_password(service, username, encrypted_password)
        print(f"Password for {service} stored.")

    def get_password(self):
        service = input("Enter service URL or name to retrieve password for: ")
        username = input("Enter username or email to retrieve password for: ")

        encrypted_password = self.db_manager.get_password(service, username)

        if encrypted_password:
            decrypted_password = self.encryption_handler.decrypt(encrypted_password)
            print(f"Password for {service} (username {username}): {decrypted_password}")
        else:
            print(f"No password found for {service} and username {username}")
            print("Make sure there are no typos in the service name or username and try again.")
    
    def delete_password(self):
        service = input("Enter service URL or name to delete password for: ")
        username = input("Enter username or email to delete password for: ")

        self.db_manager.delete_password(service, username)
        print(f"Password for {service} with username {username} deleted.")

    def update_password(self):
        service = input("Enter service URL or name to update password for: ")
        username = input("Enter username or email to update password for: ")
        new_password = getpass.getpass("Enter new password: ")

        encrypted_password = self.encryption_handler.encrypt(new_password)

        self.db_manager.update_password(service, username, encrypted_password)
        print(f"Password for {service} updated.")

    def list_services(self):
        stored_information = self.db_manager.retrieve_stored_information()

        if stored_information:
            print("\nStored services and usernames:\n")

            for service, username in stored_information:
                print(f"Service: {service} | Username: {username}")
        else:
            print("No services stored.")