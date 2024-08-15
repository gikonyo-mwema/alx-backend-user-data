#!/usr/bin/env python3
"""
User module that defines the User model for the database.
Creates a User model that maps to the 'users' table.
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create an SQLite database engine
engine = create_engine('sqlite:///users.db')

# Define a base class for declarative models
Base = declarative_base()


class User(Base):
    """
    User model representing the 'users' table in the database.

    Attributes:
        id (int): The primary key for the user.
        email (str): The email of the user, must not be null.
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID for the user, can be null.
        reset_token (str): The password reset token for the user, can be null.
    """

    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)  # Primary key
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)


# Create the tables in the database
Base.metadata.create_all(engine)
