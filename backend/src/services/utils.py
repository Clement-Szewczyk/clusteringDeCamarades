"""
Utility functions and decorators shared across service modules.
"""

from flask import current_app

def ensure_app_context(func):
    """
    Decorator to ensure database operations run in an app context.
    This prevents the common issue of attempting database operations
    outside of a Flask application context.
    """
    def wrapper(*args, **kwargs):
        try:
            # Check if we're already in an app context
            current_app._get_current_object()
            return func(*args, **kwargs)
        except RuntimeError:
            # If not, get the app and create a context
            from app import get_app
            app = get_app()
            with app.app_context():
                return func(*args, **kwargs)
    return wrapper
