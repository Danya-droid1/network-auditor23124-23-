"""
Authentication module for user login and session management.

Author: Golub Daniil Nikolaevich
"""

import bcrypt
from src.core.database_manager import DatabaseManager, User

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def authenticate(self, username: str, password: str) -> dict:
        # Authenticate user and return user data or None
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and user.is_active:
                if self.verify_password(password, user.password_hash):
                    return {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role.name if user.role else "unknown",
                        "full_name": user.full_name
                    }
        finally:
            session.close()
        return None

    def hash_password(self, password: str) -> str:
        # Generate a bcrypt hash for a plain text password
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')