"""
Utility functions and decorators shared across service modules.

This module provides common utilities that are used throughout the application's service layer,
including decorators for handling application context and other shared helper functions.
"""

from flask import current_app

def ensure_app_context(func):
    """
    Decorator to ensure database operations run in an app context.
    
    This prevents the common issue of attempting database operations
    outside of a Flask application context by creating one if needed.
    
    Args:
        func (callable): The function to wrap with app context handling
        
    Returns:
        callable: The wrapped function that will always execute within an app context
        
    Example:
        @ensure_app_context
        def my_database_function():
            # Database operations here
            pass
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
