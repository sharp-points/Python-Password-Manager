import sqlite3

class DatabaseManager:
    def __init__(self, db_file='password_manager.db'):
        self.connection = sqlite3.connect(db_file)
        self._initialize_database()

    def _initialize_database(self):
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS stored_passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password BLOB NOT NULL
            )
        ''')

        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS master_password (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_hash TEXT NOT NULL
            )
        ''')

        self.connection.commit()

    def store_password(self, service, username, password):
        self.connection.execute('''
            INSERT INTO stored_passwords (service, username, password)
            VALUES (?, ?, ?)
        ''', (service, username, password))

        self.connection.commit()

    def get_password(self, service, username):
        cursor = self.connection.cursor()

        cursor.execute('''
            SELECT password
            FROM stored_passwords
            WHERE service = ? AND username = ?
        ''', (service, username))

        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            print(f"No password found for {service} and {username}")

    def update_password(self, service, username, password):
        self.connection.execute('''
            UPDATE stored_passwords
            SET password = ?
            WHERE service = ? AND username = ?
        ''', (password, service, username))

        self.connection.commit()
    
    def delete_password(self, service, username):
        self.connection.execute('''
            DELETE FROM stored_passwords
            WHERE service = ? AND username = ?
        ''', (service, username))

        self.connection.commit()
    
    def retrieve_stored_information(self):
        cursor = self.connection.cursor()

        cursor.execute('SELECT service, username FROM stored_passwords')

        rows = cursor.fetchall()

        return rows
    
    def store_master_hash(self, master_hash):
        self.connection.execute('''
            INSERT INTO master_password
            (master_hash) VALUES (?)
        ''', (master_hash,))

        self.connection.commit()

    def get_master_hash(self):
        cursor = self.connection.cursor()

        cursor.execute('''
            SELECT master_hash
            FROM master_password
            WHERE id = 1
        ''')

        result = cursor.fetchone()

        if result:
            return result
        else:
            return None