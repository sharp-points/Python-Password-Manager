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
            master_hash TEXT NOT NULL
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
        VALUES (?, ?, ?)
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

def store_master_password_hash(password_hash):
    # Create connection to SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO master_password
        (master_hash) VALUES (?)
    ''', (password_hash,))

    # Commit and close connection
    connection.commit()
    connection.close()

def get_master_password_hash():
    # Create connection to SQLite database "password_manager.db"
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    # Select password for given url and username
    cursor.execute('''
        SELECT master_hash
        FROM master_password
        WHERE id = 1
    ''')

    result = cursor.fetchone()
    connection.close()

    if result:
        return result
    else:
        print(f"No password hash found.")
    
def is_first_time_use():
    connection = sqlite3.connect('password_manager.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM master_password')
    result = cursor.fetchone()
    connection.close()

    # Returns True if no master password exists
    return result[0] == 0  