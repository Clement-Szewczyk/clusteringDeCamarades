"""
Formular Service Module.

This module provides services for managing formular (form) entities,
including CRUD operations and teacher-specific form retrievals.
A formular represents a voting form that teachers can create for students.
"""

from flask import request, current_app
from models.formular import Formular
from extensions import db
from datetime import datetime
from services.utils import ensure_app_context

class FormularService:
    """
    Service class for handling formular-related operations.
    
    This class provides methods for formular management including creating,
    retrieving, updating, and deleting formular records.
    """
    
    @staticmethod
    @ensure_app_context
    def get_all_formular():
        """
        Retrieves all formulars from the database.
        
        Returns:
            list: A list of dictionaries containing formular information
        """
        formulars = Formular.query.all()
        return [formular.to_dict() for formular in formulars]
    
    @staticmethod
    @ensure_app_context
    def get_all_teacher_formular(teacher_id):
        """
        Retrieves all formulars created by a specific teacher.
        
        Args:
            teacher_id (int): The ID of the teacher
            
        Returns:
            list: A list of dictionaries containing the teacher's formulars
        """
        formulars = Formular.query.filter_by(formular_creator=teacher_id).all()
        return [formular.to_dict() for formular in formulars]

    @staticmethod
    def create_formular():
        """
        Creates a new formular based on the request data.
        
        Expects a JSON body with 'title', 'description', 'creator_id',
        'end_date', and 'nb_person_group' fields.
        
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is either the new formular data or an error message
            - status_code is the HTTP status code (201 for success)
            
        Raises:
            Exception: If database operations fail
        """
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
    @ensure_app_context
    def get_formular(formular_id):
        """
        Retrieves a formular by ID.
        
        Args:
            formular_id (int): The ID of the formular to retrieve
            
        Returns:
            dict: The formular data if found, None otherwise
        """
        formular = Formular.query.get(formular_id)
        if formular:
            return formular.to_dict()
        return None
    
    @staticmethod
    @ensure_app_context
    def update_formular(formular_id):
        """
        Updates an existing formular identified by ID.
        
        Args:
            formular_id (int): The ID of the formular to update
            
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is either the updated formular data or an error message
            - status_code is the HTTP status code (200 for success, 404 if not found)
            
        Raises:
            Exception: If database operations fail
        """
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
    @ensure_app_context
    def delete_formular(formular_id):
        """
        Deletes a formular by ID.
        
        Args:
            formular_id (int): The ID of the formular to delete
            
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is a success or error message
            - status_code is the HTTP status code (204 for success, 404 if not found)
            
        Raises:
            Exception: If database operations fail
        """
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

