#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


from user import User, Base


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
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # Create a new User instance
        self._session.add(new_user)  # Add the user to the session
        self._session.commit()  # Commit the session to save the user
        return new_user  # Return the created User object

    def find_user_by(self, **kwargs) -> User:
        """Find a user by the given attributes.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The found user object.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If an invalid keyword argument is provided.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except InvalidRequestError:
            raise InvalidRequestError
        except NoResultFound:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments for user attributes update

        Raises:
            ValueError: If an invalid attribute is passed.
        """
        # Find the user by ID
        user = self.find_user_by(id=user_id)

        # Allowed attributes to update
        valid_attributes = {
            'email',
            'hashed_password',
            'session_id',
            'reset_token'
        }

        # Update user attributes based on kwargs
        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)  # Update the user's attribute

        # Commit the changes to the database
        self._session.commit()
