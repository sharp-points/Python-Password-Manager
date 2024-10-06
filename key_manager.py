import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class KeyManager:
    def __init__(self, salt_file = 'salt.bin'):
        self.salt_file = salt_file
        self.salt = self._load_or_generate_salt()

    def _load_or_generate_salt(self):
        if os.path.exists(self.salt_file):
            with open(self.salt_file, 'rb') as file:
                return file.read()
        else:
            new_salt = os.urandom(16)
            with open(self.salt_file, 'wb') as file:
                file.write(new_salt)
            return new_salt
    
    def derive_key(self, master_password):
        kdf = PBKDF2HMAC (
            algorithm=hashes.SHA256(),
            length=32, #The desired length of the derived key in bytes. AES-256 requires 32 bytes.
            salt=self.salt,
            iterations=480000,
            backend=default_backend()
        )

        return kdf.derive(master_password.encode())
