from extensions import db
from models.auth_user import AuthUser
from models.role import Role
from models.student import Student
from models.teacher import Teacher
from models.formular import Formular
from models.vote import Vote
from models.user_role import UserRole
from flask import current_app

def init_db(app=None):
    """Initialize the database with tables"""
    if app is None:
        # If no app is provided, try to use the current_app
        app = current_app
        
    with app.app_context():
        db.create_all()
        
        # Create default roles
        admin_role = Role(role_name="admin")
        teacher_role = Role(role_name="teacher") 
        student_role = Role(role_name="student")
        
        db.session.add_all([admin_role, teacher_role, student_role])
        db.session.commit()

    
    
    print("Database initialized successfully")

if __name__ == "__main__":
    # When run directly, import app and use it
    from app import create_app
    app = create_app()
    init_db(app)
