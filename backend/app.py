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
    """Returns the application instance, useful for database operations outside request context"""
    global _app
    if _app is not None:
        return _app
    return current_app

def create_app(config_name='default'):
    """Application factory function"""
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
        return jsonify({'error': 'Not found'}), 404
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Server error'}), 500
    
        
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG', 'development'))
    app.run(debug=True)