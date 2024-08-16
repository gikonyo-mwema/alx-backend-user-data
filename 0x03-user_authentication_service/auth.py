#!/usr/bin/env python3
"""Auth module
"""
import uuid
from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the Auth class with a database instance."""
        self._db = DB()

    def _generate_uuid(self) -> str:
        """Generate a new UUID.

        Returns:
            str: A string representation of a new UUID.
        """
        return str(uuid.uuid4())

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
        salt = gensalt()
        hashed_password = hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        # Check if the user already exists
        try:
            self._db.find_user_by(email=email)  # Attempt to find the user
            raise ValueError(f"User {email} already exists")  # User found
        except NoResultFound:
            # User does not exist, proceed to create a new one
            hashed_password = self._hash_password(password)  # Hash password
            user = self._db.add_user(email, hashed_password)  # Save the user
            return user  # Return the created User object

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user's login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)  # Find user by email
            # Check if the password matches the stored hash
            if checkpw(password.encode('utf-8'), user.hashed_password):
                return True  # Password matches
            return False  # Password does not match
        except NoResultFound:
            return False  # User not found

    def create_session(self, email: str) -> str:
        """Create a session for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID for the user.
        """
        try:
            user = self._db.find_user_by(email=email)  # Find user by email
            session_id = self._generate_uuid()  # Generate a new UUID
            user.session_id = session_id  # Set the session ID
            self._db._session.commit()  # Commit the changes
            return session_id  # Return the session ID
        except NoResultFound:
            return None  # User not found

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get a user from their session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            User: The corresponding User object or None.
        """
        if session_id is None:
            return None  # Session ID is None
        try:
            user = self._db.find_user_by(session_id=session_id)  # Find user
            return user  # Return the user
        except NoResultFound:
            return None  # User not found

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session.

        Args:
            user_id (int): The ID of the user.
        """
        user = self._db.find_user_by(id=user_id)  # Find user by ID
        user.session_id = None  # Set session ID to None
        self._db._session.commit()  # Commit the changes

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)  # Find user by email
            reset_token = self._generate_uuid()  # Generate a new UUID
            user.reset_token = reset_token  # Set the reset token
            self._db._session.commit()  # Commit the changes
            return reset_token  # Return the reset token
        except NoResultFound:
            raise ValueError("User not found")  # User does not exist

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password using a reset token.

        Args:
            reset_token (str): The reset token of the user.
            password (str): The new password of the user.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)  # Find user
            hashed_password = self._hash_password(password)  # Hash password
            user.hashed_password = hashed_password  # Update password
            user.reset_token = None  # Clear reset token
            self._db._session.commit()  # Commit the changes
        except NoResultFound:
            raise ValueError("User not found")  # User does not exist
