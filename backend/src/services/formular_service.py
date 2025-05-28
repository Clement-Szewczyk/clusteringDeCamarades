from flask import request, current_app, g
from models.formular import Formular
from models.role import Role
from models.user_role import UserRole
from extensions import db
from datetime import datetime
from services.auth_middleware import token_required

class FormularService:
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
    def get_all_formulars():
        """Retrieves all formulars"""
        formulars = Formular.query.all()
        return [formular.to_dict() for formular in formulars]
    
    @staticmethod
    @_ensure_app_context
    def get_formular(formular_id):
        """Retrieves a formular by ID"""
        formular = Formular.query.get(formular_id)
        if formular:
            return formular.to_dict()
        return None
    
    @staticmethod
    def validate_formular_data(data):
        """Validates formular data"""
        errors = []
        
        required_fields = ['formular_title', 'formular_description', 'formular_creator', 
                           'formular_start', 'formular_end', 'formular_nb_vote_per_person']
        
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required")
        
        if not errors:
            # Validate date formats
            try:
                start_date = datetime.fromisoformat(data['formular_start'])
                end_date = datetime.fromisoformat(data['formular_end'])
                
                # Check if start is before end
                if start_date >= end_date:
                    errors.append("Start date must be before end date")
            except ValueError:
                errors.append("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
            
            # Check if number of votes per person is positive
            if 'formular_nb_vote_per_person' in data and data['formular_nb_vote_per_person'] <= 0:
                errors.append("Number of votes per person must be positive")
        
        return errors
    
    @staticmethod
    @token_required
    def create_formular():
        """Creates a new formular"""
        # Check if user is a teacher
        current_user = g.current_user
        
        # Get user role
        user_role = UserRole.query.filter_by(user_role_userid=current_user['user_id']).first()
        role = Role.query.get(user_role.user_role_roleid) if user_role else None
        
        if not role or role.role_name != 'teacher':
            return {'error': 'Permission denied. Only teachers can create forms'}, 403
        
        data = request.get_json()
        
        if not data:
            return {'error': 'No data provided'}, 400
        
        # Validate the formular data
        errors = FormularService.validate_formular_data(data)
        if errors:
            return {'error': errors}, 400
        
        # Create new formular
        try:
            new_formular = Formular(
                formular_title=data['formular_title'],
                formular_description=data['formular_description'],
                formular_creator=current_user['user_id'],  # Use current user's ID
                formular_start=datetime.fromisoformat(data['formular_start']),
                formular_end=datetime.fromisoformat(data['formular_end']),
                formular_nb_vote_per_person=data['formular_nb_vote_per_person']
            )
            db.session.add(new_formular)
            db.session.commit()
            return new_formular.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create formular: {str(e)}'}, 500
    
    @staticmethod
    @_ensure_app_context
    def update_formular(formular_id):
        """Updates an existing formular"""
        data = request.get_json()
        
        if not data:
            return {'error': 'No data provided'}, 400
        
        # Check if formular exists
        formular = Formular.query.get(formular_id)
        if not formular:
            return {'error': 'Formular not found'}, 404
        
        # Validate fields that are present in the data
        errors = []
        if 'formular_start' in data and 'formular_end' in data:
            try:
                start_date = datetime.fromisoformat(data['formular_start'])
                end_date = datetime.fromisoformat(data['formular_end'])
                if start_date >= end_date:
                    errors.append("Start date must be before end date")
            except ValueError:
                errors.append("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        elif 'formular_start' in data:
            try:
                start_date = datetime.fromisoformat(data['formular_start'])
                if start_date >= formular.formular_end:
                    errors.append("Start date must be before end date")
            except ValueError:
                errors.append("Invalid date format for start date")
        elif 'formular_end' in data:
            try:
                end_date = datetime.fromisoformat(data['formular_end'])
                if formular.formular_start >= end_date:
                    errors.append("Start date must be before end date")
            except ValueError:
                errors.append("Invalid date format for end date")
        
        if 'formular_nb_vote_per_person' in data and data['formular_nb_vote_per_person'] <= 0:
            errors.append("Number of votes per person must be positive")
        
        if errors:
            return {'error': errors}, 400
        
        # Update formular fields
        try:
            if 'formular_title' in data:
                formular.formular_title = data['formular_title']
            if 'formular_description' in data:
                formular.formular_description = data['formular_description']
            if 'formular_creator' in data:
                formular.formular_creator = data['formular_creator']
            if 'formular_start' in data:
                formular.formular_start = datetime.fromisoformat(data['formular_start'])
            if 'formular_end' in data:
                formular.formular_end = datetime.fromisoformat(data['formular_end'])
            if 'formular_nb_vote_per_person' in data:
                formular.formular_nb_vote_per_person = data['formular_nb_vote_per_person']
                
            db.session.commit()
            return formular.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to update formular: {str(e)}'}, 500
    
    @staticmethod
    @_ensure_app_context
    def delete_formular(formular_id):
        """Deletes a formular by ID"""
        formular = Formular.query.get(formular_id)
        if not formular:
            return {'error': 'Formular not found'}, 404
        
        try:
            db.session.delete(formular)
            db.session.commit()
            return {'message': 'Formular deleted successfully'}, 204
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete formular: {str(e)}'}, 500
