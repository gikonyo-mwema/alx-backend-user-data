#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome() -> dict:
    """Return a welcome message in JSON format.

    Returns:
        dict: A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> dict:
    """Register a new user.

    Returns:
        dict: A JSON response with the registered email and a message.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        abort(400, description="email already registered")


@app.route("/sessions", methods=["POST"])
def login() -> dict:
    """Log in a user and create a session.

    Returns:
        dict: A JSON response with the user email and a message.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)  # Unauthorized

    session_id = AUTH.create_session(email)  # Create a session
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)  # Set session ID cookie
    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> dict:
    """Log out a user by destroying the session.

    Returns:
        dict: A JSON response indicating the logout.
    """
    session_id = request.cookies.get("session_id")  # session ID from cookie
    if session_id is None:
        abort(403)  # Forbidden

    user = AUTH.get_user_from_session_id(session_id)  # Find user by session ID
    if user is None:
        abort(403)  # Forbidden

    AUTH.destroy_session(user.id)  # Destroy the session
    return jsonify({"message": "logged out"})


@app.route("/profile", methods=["GET"])
def profile() -> dict:
    """Get the user profile.

    Returns:
        dict: A JSON response with the user's email.
    """
    session_id = request.cookies.get("session_id")  # session ID from cookie
    user = AUTH.get_user_from_session_id(session_id)  # Find user

    if user is None:
        abort(403)  # Forbidden

    return jsonify({"email": user.email})  # Return user email


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> dict:
    """Generate a reset password token for a user.

    Returns:
        dict: A JSON response with the user's email and reset token.
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)  # Generate token
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)  # Forbidden


@app.route("/reset_password", methods=["PUT"])
def update_password() -> dict:
    """Update the user's password.

    Returns:
        dict: A JSON response indicating the password update.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)  # Update password
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)  # Forbidden


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
