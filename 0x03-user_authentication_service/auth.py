#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
import uuid
from db import DB

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _generate_uuid(self) -> str:
        """Generate a new UUID

        Returns:
            str: a string representation of a new UUID
        """
        return str(uuid.uuid4())

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email (str): The user's email address
            password (str): The user's password

        Raises:
            ValueError: if user already exists

        Returns:
            User: the newly created user
        """
        try:
            self._db.find_user_by_email(email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_id = self._generate_uuid()
            user = self._db.add_user(user_id, email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login is valid

        Args:
            email (str): The user's email
            password (str): The user's password

        Returns:
            bool: True if the login is valid, False otherwise
        """
        try:
            user = self._db.find_user_by_email(email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for the user

        Args:
            email (str): The user's email

        Returns:
            str: the session ID
        """
        try:
            user = self._db.find_user_by_email(email)
            session_id = self._generate_uuid()
            self._db.update_user_session_id(user.id, session_id)
            return session_id
        except NoResultFound:
            return ""

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns the user corresponding to the session ID or None"""
        if session_id is None:
            return None

        user_id = self._db.find_user_id_by_session_id(session_id)
        if user_id is None:
            return None

        user = self._db.find_user_by_id(user_id)
        return user
