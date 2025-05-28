"""
Student Model.

This module defines the Student model which represents student users
in the system and tracks their email information.
"""

from extensions import db

class Student(db.Model):
    """
    Student database model for storing student information.
    
    This model tracks students who can participate in voting forms. It contains
    the student's email address and maintains a relationship with votes they receive.
    
    Attributes:
        student_id (int): Primary key, unique identifier for the student
        student_email (str): Student's email address, unique constraint
    """
    __tablename__ = 'student'
    
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_email = db.Column(db.String(255), unique=True, nullable=False)
    
    # Relationship with Vote model
    votes = db.relationship('Vote', backref='student', lazy=True)
    
    def __repr__(self):
        """String representation of the Student object."""
        return f"<Student {self.student_email}>"
    
    def to_dict(self):
        """
        Convert the Student object to a dictionary.
        
        Returns:
            dict: Dictionary containing student data
        """
        return {
            'student_id': self.student_id,
            'student_email': self.student_email
        }
