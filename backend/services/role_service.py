from flask import request, current_app
from models.role import Role
from extensions import db

class RoleService:
    @staticmethod
    def _ensure_app_context(func):
        """Decorator to ensure database operations run in an app context"""
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
    
    @staticmethod
    @_ensure_app_context
    def get_all_roles():
        """Retrieves all roles"""
        roles = Role.query.all()
        return [role.to_dict() for role in roles]
    
    @staticmethod
    @_ensure_app_context
    def get_role(role_id):
        """Retrieves a role by ID"""
        role = Role.query.get(role_id)
        if role:
            return role.to_dict()
        return None
    
    @staticmethod
    def create_role():
        """Creates a new role"""
        data = request.get_json()
        
        if not data or 'role_name' not in data:
            return {'error': 'Role name is required'}, 400
        
        role_name = data['role_name']
        
        # Check if role with this name already exists
        existing_role = Role.query.filter_by(role_name=role_name).first()
        if existing_role:
            return {'error': 'Role with this name already exists'}, 409
        
        # Create new role
        try:
            new_role = Role(role_name=role_name)
            db.session.add(new_role)
            db.session.commit()
            return new_role.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create role: {str(e)}'}, 500
    
    