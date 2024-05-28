from db import DB
import bcrypt

class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> "User":
        """
        Register a new user.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.

        Raises:
            ValueError: If a user with the given email already exists.

        Returns:
            User: The newly created user.
        """
        # Check if a user with the given email already exists
        if self._db.find_user_by(email=email):
            raise ValueError(f"User {email} already exists")

        # Hash the password
        hashed_password = self._hash_password(password)

        # Create the new user and save it to the database
        user = self._db.add_user(email, hashed_password)
        return user

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The salted hash of the input password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password
