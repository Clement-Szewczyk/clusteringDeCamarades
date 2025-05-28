"""
Main Application Module.

This module contains the Flask application factory and configuration setup.
It initializes the application, registers routes, sets up error handlers,
and provides utility functions for accessing the application instance.
"""

from flask import Flask, jsonify, redirect, current_app
from flask_restful import Api
from flask_cors import CORS
from extensions import db  # Importer db depuis extensions
import os
from config.config import config
from dotenv import load_dotenv

# Global variable to store the application instance
_app = None

def get_app():
    """
    Returns the application instance, useful for database operations outside request context.
    
    Returns:
        Flask: The Flask application instance
    """
    global _app
    if _app is not None:
        return _app
    return current_app

def create_app(config_name='default'):
    """
    Application factory function that creates and configures the Flask application.
    
    Args:
        config_name (str): The configuration to use ('development', 'testing', 'production')
        
    Returns:
        Flask: The configured Flask application instance
    """
    global _app
    
    load_dotenv()
    app = Flask(__name__)
    
    # Store the app instance globally
    _app = app
    
    # Load configuration
    app_config = config[config_name]
    app.config.from_object(app_config)
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app)
    
    # Initialize API
    api = Api(app)
    
    # Register routes
    from routes import register_routes
    register_routes(app, api)
    
    # Create tables
    with app.app_context():
        db.create_all()


    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        """
        Handle 404 Not Found errors.
        
        Args:
            error: The error object
            
        Returns:
            tuple: JSON response with error message and status code
        """
        return jsonify({'error': 'Not found'}), 404
        
    @app.errorhandler(500)
    def server_error(error):
        """
        Handle 500 Server Error.
        
        Args:
            error: The error object
            
        Returns:
            tuple: JSON response with error message and status code
        """
        return jsonify({'error': 'Server error'}), 500
    
        
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG', 'development'))
    app.run(debug=True)