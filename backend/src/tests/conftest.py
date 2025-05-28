import os
import pytest
import tempfile
from app import create_app
from extensions import db
from models.role import Role
from models.auth_user import AuthUser
from models.student import Student
from models.teacher import Teacher
from models.user_role import UserRole
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Create the database and the tables
    with app.app_context():
        db.create_all()
        # Create test roles
        roles = [
            Role(role_name="admin"),
            Role(role_name="teacher"),
            Role(role_name="student")
        ]
        db.session.add_all(roles)
        db.session.commit()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    """Initialize test database with sample data."""
    with app.app_context():
        # Clear existing data first to avoid unique constraint violations
        UserRole.query.delete()
        AuthUser.query.delete()
        Student.query.delete()
        Teacher.query.delete()
        db.session.commit()
        
        # Create test student
        test_student = Student(student_email="student@test.com")
        db.session.add(test_student)
        
        # Create test teacher
        test_teacher = Teacher(teacher_email="teacher@test.com")
        db.session.add(test_teacher)
        
        # Create test user with student role
        test_user = AuthUser(
            auth_user_email="student@test.com",
            auth_user_mdp=generate_password_hash("Password123"),
            auth_user_name="Test",
            auth_user_firstname="Student"
        )
        db.session.add(test_user)
        db.session.flush()  # Get the user ID
        
        # Assign student role
        student_role = Role.query.filter_by(role_name="student").first()
        user_role = UserRole(
            user_role_userid=test_user.auth_user_id,
            user_role_roleid=student_role.role_id
        )
        db.session.add(user_role)
        
        # Commit changes
        db.session.commit()
    
    yield
