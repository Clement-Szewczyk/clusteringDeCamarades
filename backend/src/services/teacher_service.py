"""
Teacher Service Module.

This module provides services for managing teacher entities,
including CRUD operations and batch processing capabilities.
"""

from flask import request, current_app
from models.teacher import Teacher
from extensions import db
import re
from services.utils import ensure_app_context

class TeacherService:
    """
    Service class for handling teacher-related operations.
    
    This class provides methods for teacher management including retrieving,
    creating, updating, and deleting teacher records, as well as batch operations.
    """
    
    @staticmethod
    def validate_email(email):
        """
        Validates email format using regex pattern.
        
        Args:
            email (str): The email address to validate
            
        Returns:
            bool: True if the email format is valid, False otherwise
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    @ensure_app_context
    def get_all_teachers():
        """
        Retrieves all teachers from the database.
        
        Returns:
            list: A list of dictionaries containing teacher information
        """
        teachers = Teacher.query.all()
        return [teacher.to_dict() for teacher in teachers]
    
    @staticmethod
    @ensure_app_context
    def get_teacher(email):
        """
        Retrieves a teacher by email address.
        
        Args:
            email (str): The email address of the teacher to retrieve
            
        Returns:
            dict: The teacher data if found, None otherwise
        """
        teacher = Teacher.query.get(email)
        if teacher:
            return teacher.to_dict()
        return None
    
    @staticmethod
    def create_teacher():
        """
        Creates a new teacher based on the request data.
        
        Expects a JSON body with 'email' field.
        
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is either the new teacher data or an error message
            - status_code is the HTTP status code (201 for success)
            
        Raises:
            Exception: If database operations fail
        """
        data = request.get_json()
        
        if not data or 'email' not in data:
            return {'error': 'Email is required'}, 400
        
        email = data['email']
        
        # Validate email
        if not TeacherService.validate_email(email):
            return {'error': 'Invalid email format'}, 400
        
        # Check if email already exists
        existing_teacher = Teacher.query.get(email)
        if existing_teacher:
            return {'error': 'Teacher with this email already exists'}, 409
        
        # Create new teacher
        try:
            new_teacher = Teacher(teacher_email=email)
            db.session.add(new_teacher)
            db.session.commit()
            return new_teacher.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create teacher: {str(e)}'}, 500
    
    @staticmethod
    def create_teachers_batch():
        """
        Creates multiple teachers in a single request.
        
        Expects a JSON array of objects, each with an 'email' field.
        
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data includes lists of successful and failed operations
            - status_code is the HTTP status code (207 for partial success)
            
        Raises:
            Exception: If database operations fail completely
        """
        data = request.get_json()
        
        if not isinstance(data, list):
            return {'error': 'Expected a list of teacher data'}, 400
        
        results = {
            'success': [],
            'failed': []
        }
        
        for item in data:
            if not isinstance(item, dict) or 'email' not in item:
                results['failed'].append({'data': item, 'reason': 'Missing email field'})
                continue
            
            email = item['email']
            
            # Validate email
            if not TeacherService.validate_email(email):
                results['failed'].append({'data': item, 'reason': 'Invalid email format'})
                continue
            
            # Check if email already exists
            existing_teacher = Teacher.query.get(email)
            if existing_teacher:
                results['failed'].append({'data': item, 'reason': 'Email already exists'})
                continue
            
            # Create new teacher
            try:
                new_teacher = Teacher(teacher_email=email)
                db.session.add(new_teacher)
                results['success'].append(new_teacher.to_dict())
            except Exception as e:
                results['failed'].append({'data': item, 'reason': f'Database error: {str(e)}'})
        
        # Commit or rollback based on results
        if results['success']:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': f'Failed to commit changes: {str(e)}'}, 500
        else:
            db.session.rollback()
        
        return results, 207 if results['failed'] else 201
    
    @staticmethod
    @ensure_app_context
    def update_teacher(email):
        """
        Updates an existing teacher identified by email.
        
        Args:
            email (str): The email address of the teacher to update
            
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is either the updated teacher data or an error message
            - status_code is the HTTP status code (200 for success, 404 if not found)
            
        Raises:
            Exception: If database operations fail
        """
        data = request.get_json()
        
        if not data or 'email' not in data:
            return {'error': 'Email is required'}, 400
        
        new_email = data['email']
        
        # Validate email
        if not TeacherService.validate_email(new_email):
            return {'error': 'Invalid email format'}, 400
        
        # Check if teacher exists
        teacher = Teacher.query.get(email)
        if not teacher:
            return {'error': 'Teacher not found'}, 404
        
        # Check if new email already exists (if changing email)
        if email != new_email and Teacher.query.get(new_email):
            return {'error': 'Another teacher with this email already exists'}, 409
        
        # Update teacher
        try:
            # Since email is the primary key, we need to delete and recreate
            if email != new_email:
                db.session.delete(teacher)
                new_teacher = Teacher(teacher_email=new_email)
                db.session.add(new_teacher)
                db.session.commit()
                return new_teacher.to_dict(), 200
            else:
                return teacher.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to update teacher: {str(e)}'}, 500
    
    @staticmethod
    @ensure_app_context
    def delete_teacher(email):
        """
        Deletes a teacher by email.
        
        Args:
            email (str): The email address of the teacher to delete
            
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is a success or error message
            - status_code is the HTTP status code (204 for success, 404 if not found)
            
        Raises:
            Exception: If database operations fail
        """
        teacher = Teacher.query.get(email)
        if not teacher:
            return {'error': 'Teacher not found'}, 404
        
        try:
            db.session.delete(teacher)
            db.session.commit()
            return {'message': 'Teacher deleted successfully'}, 204
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete teacher: {str(e)}'}, 500
