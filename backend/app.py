from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
import os
from config.config import config
# Import resources
from routes import register_routes

# Initialize extensions


def create_app(config_name='default'):
    # Initialize app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    CORS(app)
    
    # Initialize API
    api = Api(app)
    
    # Register routes
    register_routes(app, api)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG', 'testing'))
    app.run(debug=True)