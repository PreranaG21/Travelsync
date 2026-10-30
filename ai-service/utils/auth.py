import hashlib
import os

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2 with SHA-256 and a random salt."""
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return f"{salt}${key}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a password against the stored hash format salt$key."""
    try:
        if "$" not in stored_password:
            # Fallback for plain sha256
            return hashlib.sha256(provided_password.encode('utf-8')).hexdigest() == stored_password
        salt, key = stored_password.split("$", 1)
        new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return new_key == key
    except Exception:
        return False
