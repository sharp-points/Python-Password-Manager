import os
import bcrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class EncryptionHandler:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plain_text):
        init_vector = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(init_vector), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(plain_text.encode()) + encryptor.finalize()
        return (init_vector + encrypted_text)
    
    def decrypt(self, encrypted_text):
        init_vector = encrypted_text[:16]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(init_vector), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(encrypted_text[16:]) + decryptor.finalize()
        return decrypted_text.decode()
    
    def hash_master_password(self, master_password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(master_password.encode(), salt)
        return password_hash