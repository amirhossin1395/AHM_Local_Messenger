# 🔐 AHM Local Messenger - Encryption
# © C2026-AMIRHOSSEINHAJIMORADKHANI (AHM)

import hashlib
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from config import Config

class Encryption:
    def __init__(self):
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self):
        """گرفتن یا ساخت کلید"""
        key_file = '.encryption_key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt(self, text: str) -> str:
        """رمزنگاری متن"""
        if not text:
            return text
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt(self, encrypted: str) -> str:
        """رمزگشایی متن"""
        if not encrypted:
            return encrypted
        try:
            return self.cipher.decrypt(encrypted.encode()).decode()
        except:
            return encrypted
    
    def hash_password(self, password: str, salt: str = None) -> tuple:
        """هش رمز با Salt"""
        if not salt:
            salt = base64.b64encode(os.urandom(16)).decode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000,
        )
        key = base64.b64encode(kdf.derive(password.encode())).decode()
        return key, salt
    
    def verify_password(self, password: str, hashed: str, salt: str) -> bool:
        """تایید رمز"""
        new_hash, _ = self.hash_password(password, salt)
        return new_hash == hashed
    
    def generate_token(self, length: int = 32) -> str:
        """تولید توکن امن"""
        return base64.urlsafe_b64encode(os.urandom(length)).decode()
    
    def encrypt_file(self, file_path: str) -> str:
        """رمزنگاری فایل"""
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted = self.cipher.encrypt(data)
        
        encrypted_path = file_path + '.enc'
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted)
        
        return encrypted_path
    
    def decrypt_file(self, encrypted_path: str) -> str:
        """رمزگشایی فایل"""
        with open(encrypted_path, 'rb') as f:
            data = f.read()
        
        decrypted = self.cipher.decrypt(data)
        
        original_path = encrypted_path.replace('.enc', '')
        with open(original_path, 'wb') as f:
            f.write(decrypted)
        
        return original_path

# نمونه
encryption = Encryption()