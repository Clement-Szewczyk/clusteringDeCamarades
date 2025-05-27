import os

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    os.environ.get('SECRET_KEY')
    # Utiliser SQLite comme base de données interne
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Uncomment if using Flask-Mail
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.example.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'

class ProductionConfig(Config):
    """Production configuration."""
    # Production specific settings

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
