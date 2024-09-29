import sqlite3

def initialize_database():

    # Open or create SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    # Create stored_passwords table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stored_passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_url TEXT NOT NULL,
            username TEXT NOT NULL,
            password BLOB NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_password (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            master_hash TEXT NOT NULL,
            salt BLOB NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS encrypted_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aes_key BLOB NOT NULL
        )
    ''')

    # Commit and close database connection
    connection.commit()
    connection.close()


def store_password(service_url, username, password):
    # Create connection to SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    # Insert information into database
    cursor.execute('''
        INSERT INTO stored_passwords (service_url, username, password)
        VALUES (?, ?, ?, ?)
    ''', (service_url, username, password))

    # Commit and close connection
    connection.commit()
    connection.close()

def get_password(service_url, username):
    # Create connection to SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    # Select password for given url and username
    cursor.execute('''
        SELECT password
        FROM stored_passwords
        WHERE service_url = ? AND username = ?
    ''', (service_url, username))

    result = cursor.fetchone()
    connection.close()

    if result:
        return result
    else:
        print(f"No password found for {service_url} and {username}")

def update_password(service_url, username, password):
    # Create connection to SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE stored_passwords
        SET password = ?
        WHERE service_url = ? AND username = ?
    ''', (password, service_url, username))

    # Commit and close connection
    connection.commit()
    connection.close()

def delete_password(service_url, username):
    # Create connection to SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM stored_passwords
        WHERE service_url = ? AND username = ?
    ''', (service_url, username))

    # Commit and close connection
    connection.commit()
    connection.close()

def retrieve_stored_information():
    # Create connection to SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT service_url, username FROM stored_passwords')

    rows = cursor.fetchall()

    connection.close()

    return rows