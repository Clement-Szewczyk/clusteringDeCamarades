"""
Authentication User Model.

This module defines the AuthUser model which represents authenticated users
in the system, including login credentials and personal information.
"""

from extensions import db

class AuthUser(db.Model):
    """
    AuthUser database model for storing authenticated user information.
    
    This model stores user authentication details including email, password hash,
    name, and firstname. It also maintains relationships with roles, formulars,
    and votes associated with the user.
    
    Attributes:
        auth_user_id (int): Primary key, unique identifier for the user
        auth_user_email (str): User's email address
        auth_user_mdp (str): Hashed password
        auth_user_name (str): User's last name
        auth_user_firstname (str): User's first name
    """
    __tablename__ = 'auth_user'
    
    auth_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auth_user_email = db.Column(db.String(255), nullable=False)
    auth_user_mdp = db.Column(db.String(255), nullable=False)
    auth_user_name = db.Column(db.String(100), nullable=False)
    auth_user_firstname = db.Column(db.String(100), nullable=False)
    
    # Relationships
    roles = db.relationship('UserRole', backref='user', lazy=True)
    formulars = db.relationship('Formular', backref='creator', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    
    def __repr__(self):
        """String representation of the AuthUser object."""
        return f'<AuthUser {self.auth_user_email}>'
    
    def to_dict(self):
        """
        Convert the AuthUser object to a dictionary.
        
        Returns:
            dict: Dictionary containing user data (excluding password)
        """
        return {
            'auth_user_id': self.auth_user_id,
            'auth_user_email': self.auth_user_email,
            'auth_user_name': self.auth_user_name,
            'auth_user_firstname': self.auth_user_firstname
        }
