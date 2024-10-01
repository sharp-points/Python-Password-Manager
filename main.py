import db
import password_manager

def main():
    """Main program execution."""
    # Initialize database if not already created
    db.initialize_database()

    # Check if it's the user's first time running the program
    if db.is_first_time_use():
        password_manager.first_time_setup()

    # Authenticate user before proceeding
    password_manager.authenticate_user()

    # Main menu loop
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
            password_manager.add_new_service()
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
