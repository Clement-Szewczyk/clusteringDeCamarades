from flask import request, current_app
from models.formular import Formular
from extensions import db
from datetime import datetime

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
    def get_all_formular():
        """Retrieves all formulars"""
        formulars = Formular.query.all()
        return [formular.to_dict() for formular in formulars]
    
    @staticmethod
    @_ensure_app_context
    def get_all_teacher_formular(teacher_id):
        """Retrieves all formulars created by a specific teacher"""
        formulars = Formular.query.filter_by(formular_creator=teacher_id).all()
        return [formular.to_dict() for formular in formulars]

    @staticmethod
    def create_formular():
        """Creates a new formular"""
        data = request.get_json()
        
        if not data:
            return {'error': 'No data provided'}, 400
            
        required_fields = ['title', 'description', 'creator_id', 'end_date', 'nb_person_group']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, 400
        
        try:
            # Set start date to current date if not provided
            start_date = datetime.fromisoformat(data.get('start_date')) if 'start_date' in data else datetime.now()
            end_date = datetime.fromisoformat(data['end_date'])
            
            new_formular = Formular(
                formular_title=data['title'],
                formular_description=data['description'],
                formular_creator=data['creator_id'],
                formular_start=start_date,
                formular_end=end_date,
                formular_nb_person_group=data['nb_person_group']
            )
            
            db.session.add(new_formular)
            db.session.commit()
            return new_formular.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create formular: {str(e)}'}, 500
    
    @staticmethod
    @_ensure_app_context
    def get_formular(formular_id):
        """Retrieves a formular by ID"""
        formular = Formular.query.get(formular_id)
        if formular:
            return formular.to_dict()
        return None
    
    @staticmethod
    @_ensure_app_context
    def update_formular(formular_id):
        """Updates an existing formular"""
        data = request.get_json()
        
        if not data:
            return {'error': 'No data provided'}, 400
            
        formular = Formular.query.get(formular_id)
        if not formular:
            return {'error': 'Formular not found'}, 404
            
        try:
            if 'title' in data:
                formular.formular_title = data['title']
            if 'description' in data:
                formular.formular_description = data['description']
            if 'end_date' in data:
                formular.formular_end = datetime.fromisoformat(data['end_date'])
            if 'nb_person_group' in data:
                formular.formular_nb_person_group = data['nb_person_group']
                
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

