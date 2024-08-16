#!/usr/bin/env python3
"""Integration tests for the Flask app.
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.
    """
    response = requests.post(f"{BASE_URL}/users", data={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with the wrong password.

    Args:
        email (str): The email of the user.
        password (str): The wrong password.
    """
    response = requests.post(f"{BASE_URL}/sessions", data={
        "email": email,
        "password": password
    })
    assert response.status_code == 401  # Unauthorized


def log_in(email: str, password: str) -> str:
    """Log in a user and return the session ID.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID.
    """
    response = requests.post(f"{BASE_URL}/sessions", data={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    assert "session_id" in response.cookies
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Attempt to access profile without logging in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403  # Forbidden


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in.

    Args:
        session_id (str): The session ID of the user.
    """
    response = requests.get(f"{BASE_URL}/profile", cookies={
        "session_id": session_id
    })
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Log out a user.

    Args:
        session_id (str): The session ID of the user.
    """
    response = requests.delete(f"{BASE_URL}/sessions", cookies={
        "session_id": session_id
    })
    assert response.status_code == 200
    assert response.json() == {"message": "logged out"}


def reset_password_token(email: str) -> str:
    """Request a reset password token.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset token.
    """
    response = requests.post(f"{BASE_URL}/reset_password", data={
        "email": email
    })
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update a user's password.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset token.
        new_password (str): The new password.
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
