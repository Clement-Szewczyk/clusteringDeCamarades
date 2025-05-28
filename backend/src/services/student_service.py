"""
Student Service Module.

This module provides services for managing student entities,
including CRUD operations and batch processing capabilities.
"""

from flask import request, current_app
from models.student import Student
from extensions import db
import re
from services.utils import ensure_app_context

class StudentService:
    """
    Service class for handling student-related operations.
    
    This class provides methods for student management including retrieving,
    creating, updating, and deleting student records, as well as batch operations.
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
    def get_all_students():
        """
        Retrieves all students from the database.
        
        Returns:
            list: A list of dictionaries containing student information
        """
        students = Student.query.all()
        return [student.to_dict() for student in students]
    
    @staticmethod
    @ensure_app_context
    def get_student(student_id):
        """
        Retrieves a student by ID.
        
        Args:
            student_id (int): The ID of the student to retrieve
            
        Returns:
            dict: The student data if found, None otherwise
        """
        student = Student.query.get(student_id)
        if student:
            return student.to_dict()
        return None
    
    @staticmethod
    def create_student():
        """
        Creates a new student based on the request data.
        
        Expects a JSON body with 'email' field.
        
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is either the new student data or an error message
            - status_code is the HTTP status code (201 for success)
            
        Raises:
            Exception: If database operations fail
        """
        data = request.get_json()
        
        if not data or 'email' not in data:
            return {'error': 'Email is required'}, 400
        
        email = data['email']
        
        # Validate the email
        if not StudentService.validate_email(email):
            return {'error': 'Invalid email format'}, 400
        
        # Check if the email already exists
        existing_student = Student.query.filter_by(student_email=email).first()
        if existing_student:
            return {'error': 'Student with this email already exists'}, 409
        
        # Create a new student
        try:
            new_student = Student(student_email=email)
            db.session.add(new_student)
            db.session.commit()
            return new_student.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create student: {str(e)}'}, 500
    
    @staticmethod
    def create_students_batch():
        """
        Creates multiple students in a single request.
        
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
            return {'error': 'Expected a list of student data'}, 400
        
        results = {
            'success': [],
            'failed': []
        }
        
        for item in data:
            if not isinstance(item, dict) or 'email' not in item:
                results['failed'].append({'data': item, 'reason': 'Missing email field'})
                continue
            
            email = item['email']
            
            # Validate the email
            if not StudentService.validate_email(email):
                results['failed'].append({'data': item, 'reason': 'Invalid email format'})
                continue
            
            # Check if the email already exists
            existing_student = Student.query.filter_by(student_email=email).first()
            if existing_student:
                results['failed'].append({'data': item, 'reason': 'Email already exists'})
                continue
            
            # Create a new student
            try:
                new_student = Student(student_email=email)
                db.session.add(new_student)
                db.session.flush()  #To obtain the ID without committing
                results['success'].append(new_student.to_dict())
            except Exception as e:
                results['failed'].append({'data': item, 'reason': f'Database error: {str(e)}'})
        
        # Commit ou rollback selon les résultats
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
    def update_student(student_id):
        """
        Updates an existing student identified by ID.
        
        Args:
            student_id (int): The ID of the student to update
            
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is either the updated student data or an error message
            - status_code is the HTTP status code (200 for success, 404 if not found)
            
        Raises:
            Exception: If database operations fail
        """
        data = request.get_json()
        
        if not data or 'email' not in data:
            return {'error': 'Email is required'}, 400
        
        email = data['email']
        
        # Validate the email
        if not StudentService.validate_email(email):
            return {'error': 'Invalid email format'}, 400
        
        # Check if the student exists
        student = Student.query.get(student_id)
        if not student:
            return {'error': 'Student not found'}, 404
        
        # Check if the email already exists for another student
        existing_student = Student.query.filter(Student.student_email == email, Student.student_id != student_id).first()
        if existing_student:
            return {'error': 'Another student with this email already exists'}, 409
        
        # Update student
        try:
            student.student_email = email
            db.session.commit()
            return student.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to update student: {str(e)}'}, 500
    
    @staticmethod
    @ensure_app_context
    def delete_student(student_id):
        """
        Deletes a student by ID.
        
        Args:
            student_id (int): The ID of the student to delete
            
        Returns:
            tuple: A tuple containing (response_data, status_code)
            - response_data is a success or error message
            - status_code is the HTTP status code (204 for success, 404 if not found)
            
        Raises:
            Exception: If database operations fail
        """
        student = Student.query.get(student_id)
        if not student:
            return {'error': 'Student not found'}, 404
        
        try:
            db.session.delete(student)
            db.session.commit()
            return {'message': 'Student deleted successfully'}, 204
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete student: {str(e)}'}, 500


