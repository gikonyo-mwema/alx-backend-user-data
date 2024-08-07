#!/usr/bin/env python3
"""
Class Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False for now. Path and excluded_paths will be used later.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns None. Request will be the Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None. Request will be the Flask request object.
        """
        return None
