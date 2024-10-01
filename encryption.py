from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import subprocess
import bcrypt
from dotenv import load_dotenv

def encrypt_password(key, password):
    # Generate random 16 byte initialization vector
    initialization_vector = os.urandom(16)

    # Create cipher object using AES algorithm and Cipher Feedback
    cipher = Cipher(algorithms.AES(key), modes.CFB(initialization_vector), backend = default_backend())

    # Create encryptor object to perform encryption
    encryptor = cipher.encryptor()
    
    # Convert plaintext to bytes and encrypt plaintext data
    cipher_text = encryptor.update(password.encode()) + encryptor.finalize()

    return initialization_vector + cipher_text

def decrypt_password(key, encrypted_payload):
    # Extract initialization vector (first 16 bytes)
    initialization_vector = encrypted_payload[:16]

    # Extract encrypted data
    cipher_text = encrypted_payload[16:]

    # Create cipher object using AES algorithm and Cipher Feedback
    cipher = Cipher(algorithms.AES(key), modes.CFB(initialization_vector), backend = default_backend())

    # Create decryptor object to perform decryption
    decryptor = cipher.decryptor()

    return decryptor.update(cipher_text) + decryptor.finalize()

# Generate 32-byte AES key
def generate_key():
    return os.urandom(32)

# Generate 32-byte AES key
def generate_aes_key():
    '''
    Run commands using subprocess:
    openssl - command that launches OpenSSL program
    rand - subcommand of OpenSSL that generates random bytes
    -out - flag used to specify output where data will be saved
    ./keys/aes_key.bin - file where generated data will be saved
    32 - length of random data to be generated; 32 bytes for 256-bit key
    '''
    try:
        subprocess.run(['openssl', 'rand', '-out', './keys/aes_key.bin', '32'], check = True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
def encrypt_aes_key():
    # Pull openssl password from environment variable
    load_dotenv()
    password = os.getenv('PASSWORD')
    if not password:
        raise ValueError("Error: PASSWORD environment variable not set.")
    
    '''
    Run commands using subprocess:
    openssl - command that launches OpenSSL program
    enc - tells OpenSSL to perform encryption
    -aes-256-cbc - specifies encryption algorithm and mode to be used; AES 256 encryption with Cipher Block Chaining mode
    -in - specifies input file for encryption
    ./keys/aes_key.bin - file storing raw AES key
    -out -specifies output location
    ./keys/aes_key.enc - output location of encrypted key
    -k - flag telling OpenSSL that encryption key will be derived using password
    password - password extracted from environment variable
    '''
    try:
        subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-in', './keys/aes_key.bin', '-out', './keys/aes_key.enc', '-k', password], check = True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def decrypt_aes_key():
    # Pull openssl password from environment variable
    load_dotenv()
    password = os.getenv('PASSWORD')
    if not password:
        raise ValueError("Error: PASSWORD environment variable not set.")
    
    # Decrypt AES key
    try:    
        subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-d', '-in', './keys/aes_key.enc', '-out', './keys/decrypted_key.bin', '-k', password], check = True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    # Read the decrypted AES key from the file
    try:
        with open('./keys/decrypted_key.bin', 'rb') as decrypted_file:
            aes_key = decrypted_file.read()
            return aes_key
    except FileNotFoundError:
        raise FileNotFoundError("Error: Decrypted key file not found.")

def confirm_key_integrity():
    load_dotenv()
    # Pull openssl password from environment variable
    password = os.getenv('PASSWORD')
    if not password:
        raise ValueError("Error: PASSWORD environment variable not set.")
    
    key_integrity = True
    
    # Check if encrypted key file exists
    if os.path.exists('./keys/aes_key.enc'):
        print("Encrypted AES key file successfully created.")
    else:
        print("Error: AES key file does not exist.")
        key_integrity = False
    
    # Check if encrypted key file is not empty
    if os.path.getsize('./keys/aes_key.enc') > 0:
        print("Encrypted AES key file is not empty.")
    else:
        print("Error: Encrypted AES key file is empty.")
        key_integrity = False
    
    # Decrypt file to validate data
    try:
        subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-d', '-in', './keys/aes_key.enc', '-out', './keys/decrypted_key.bin', '-k', password], check = True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    # Check if decryption was successful
    if os.path.exists('./keys/decrypted_key.bin'):

        with open('./keys/aes_key.bin', 'rb') as original_key:
            original_data = original_key.read()

        with open('./keys/decrypted_key.bin', 'rb') as decrypted_key:
            decrypted_data = decrypted_key.read()

        # Compare original key and decrypted key
        if original_data == decrypted_data:
            print("Decryption successful. Original key matches decrypted key.")
        
        else:
            print("Error: Decrypted key does not match original key.")
            key_integrity = False
    else:
        print("Error: Decyrption failed. Cannot validate key.")

    # Confirm key integrity
    if key_integrity == True:
        print("Key integrity confirmed. Safe to delete unencrypted keys.")
    else:
        print("Error: Key integrity not confirmed.")

    return key_integrity

# Remove unencrypted AES key after sucessful encryption
def remove_unencrypted_data():
    if os.path.exists('./keys/aes_key.bin'):
        os.remove('./keys/aes_key.bin')
    if os.path.exists('./keys/decrypted_key.bin'):
        os.remove('./keys/decrypted_key.bin')

def process_aes_key():
    generate_aes_key()
    encrypt_aes_key()
    print("AES key generated and encrypted.")

    if confirm_key_integrity():
        remove_unencrypted_data()
    else:
        print("Key integrity not confirmed. Skipping deletion.")

def hash_master_password(master_password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(master_password.encode(), salt)
    return password_hash
