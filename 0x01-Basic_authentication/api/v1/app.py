#!/usr/bin/env python3
"""
Main module for the API application
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth  # Import the base Auth class

# Create a Flask application instance
app = Flask(__name__)
app.register_blueprint(app_views)  # Register the app views (routes)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})  # Enable CORS

# Initialize auth variable
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()  # Create an instance of BasicAuth
else:
    auth = Auth()  # Fallback to the original Auth class


@app.before_request
def bef_req():
    """
    Filter each request before it's handled by the proper route
    """
    if auth is None:
        return
    excluded = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if auth.require_auth(request.path, excluded):
        if auth.authorization_header(request) is None:
            abort(401, description="Unauthorized")
        if auth.current_user(request) is None:
            abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler.

    Returns a JSON response with a 404 status code when a resource is not
    found.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler.

    Returns a JSON response with a 401 status code when access is
    unauthorized.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler.

    Returns a JSON response with a 403 status code when access is
    forbidden.
    """
    return jsonify({"error": "Forbidden"}), 403


# Main entry point of the application
if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)  # Run the Flask application
