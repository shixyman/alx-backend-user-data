"""DB module
"""
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The user's email
            hashed_password (str): The user's hashed password

        Returns:
            User: The created user object
        """
        new_user = User(
            email=email,
            hashed_password=hashed_password
        )
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update an existing user in the database

        Args:
            user_id (int): The ID of the user to update
            **kwargs: Keyword arguments to update the user's attributes

        Raises:
            ValueError: If an argument that does not correspond to a user attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
        except (NoResultFound, InvalidRequestError):
            return

        for attr, value in kwargs.items():
            if hasattr(User, attr):
                setattr(user, attr, value)
            else:
                raise ValueError(f"Invalid attribute: {attr}")

        self._session.commit()

    def find_user_by(self, **kwargs) -> User:
        """Find a user by one or more attributes

        Args:
            **kwargs: Keyword arguments to filter the user search

        Returns:
            User: The found user object

        Raises:
            NoResultFound: If no user is found
            InvalidRequestError: If an invalid attribute is provided
        """
        return self._session.query(User).filter_by(**kwargs).one()
    