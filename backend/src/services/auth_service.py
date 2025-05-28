from flask import request, current_app, jsonify
import jwt
from datetime import datetime, timedelta
from models.auth_user import AuthUser
from models.student import Student
from models.teacher import Teacher
from models.role import Role
from models.user_role import UserRole
from extensions import db
import re
from werkzeug.security import generate_password_hash, check_password_hash
from services.utils import ensure_app_context

class AuthService:
    @staticmethod
    def validate_email(email):
        """Validates email format"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        """Validates password strength"""
        # At least 8 characters, 1 uppercase, 1 lowercase, 1 number
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True
    
    @staticmethod
    @ensure_app_context
    def register():
        """Register a new user if their email exists in student/teacher tables"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'nom', 'prenom']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field} is required'}, 400
        
        email = data['email']
        password = data['password']
        nom = data['nom']
        prenom = data['prenom']
        
        # Validate email format
        if not AuthService.validate_email(email):
            return {'error': 'Invalid email format'}, 400
            
        # Validate password strength
        if not AuthService.validate_password(password):
            return {'error': 'Password must be at least 8 characters and contain uppercase, lowercase, and numbers'}, 400
        
        # Check if user already exists
        existing_user = AuthUser.query.filter_by(auth_user_email=email).first()
        if existing_user:
            return {'error': 'Email already registered'}, 409
        
        # Check if email exists in student or teacher tables
        student = Student.query.filter_by(student_email=email).first()
        teacher = Teacher.query.filter_by(teacher_email=email).first()
        
        if not student and not teacher:
            return {'error': 'Email not authorized for registration'}, 403
        
        # Create new user
        try:
            hashed_password = generate_password_hash(password)
            new_user = AuthUser(
                auth_user_email=email,
                auth_user_mdp=hashed_password,
                auth_user_name=nom,
                auth_user_firstname=prenom
            )
            db.session.add(new_user)
            db.session.flush()  # Get the user ID
            
            # Assign role based on which table the email was found in
            role_name = 'teacher' if teacher else 'student'
            role = Role.query.filter_by(role_name=role_name).first()
            
            if not role:
                return {'error': f'Role {role_name} not found'}, 500
                
            user_role = UserRole(
                user_role_userid=new_user.auth_user_id,
                user_role_roleid=role.role_id
            )
            db.session.add(user_role)
            db.session.commit()
            
            return {
                'message': 'User registered successfully',
                'user': {
                    'id': new_user.auth_user_id,
                    'email': new_user.auth_user_email,
                    'nom': new_user.auth_user_name,
                    'prenom': new_user.auth_user_firstname,
                    'role': role_name
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to register user: {str(e)}'}, 500
    
    @staticmethod
    @ensure_app_context
    def login():
        """Login a user"""
        try: 
            data = request.get_json()
            
            if not data or 'email' not in data or 'password' not in data:
                return {'error': 'Email and password are required'}, 400
                
            email = data['email']
            password = data['password']
            
            # Validate email format
            if not AuthService.validate_email(email):
                return {'error': 'Invalid email format'}, 400
            
            # Find user
            user = AuthUser.query.filter_by(auth_user_email=email).first()
            if not user or not check_password_hash(user.auth_user_mdp, password):
                return {'error': 'Invalid email or password'}, 401
            
            # Get user role
            user_role = UserRole.query.filter_by(user_role_userid=user.auth_user_id).first()
            role = Role.query.get(user_role.user_role_roleid) if user_role else None
            role_name = role.role_name if role else 'unknown'
            
            # Generate JWT token
            token_expiration = datetime.utcnow() + timedelta(hours=24)
            token_payload = {
                'user_id': user.auth_user_id,
                'email': user.auth_user_email,
                'role': role_name,
                'exp': token_expiration
            }
            
            token = jwt.encode(
                token_payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            
            return {
                'token': token,
                'expires': token_expiration.isoformat(),
                'user': {
                    'id': user.auth_user_id,
                    'email': user.auth_user_email,
                    'nom': user.auth_user_name,
                    'prenom': user.auth_user_firstname,
                    'role': role_name
                }
            }
        except Exception as e:
            return {'error': f'Failed to login: {str(e)}'}, 500