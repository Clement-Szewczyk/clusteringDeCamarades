import requests
from datetime import datetime, timedelta
import os
import sys

# Add the backend/src directory to the Python path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_ajout():

    url = "http://localhost:5000/students"
    student_data = {
        "email": "test@example.com",
    }
    print("\nTesting student addition...")
    response = requests.post(url, json=student_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201

def test_prof():
        url = "http://localhost:5000/teachers"
        student_data = {
            "email": "prof@example.com",
        }
        print("\nTesting student addition...")
        response = requests.post(url, json=student_data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    

def add_role(role_name):
    """Add a role to the database"""
    url = "http://localhost:5000/roles"
    role_data = {
        "role_name": role_name
    }
    
    print(f"\nTesting adding role '{role_name}'...")
    response = requests.post(url, json=role_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201


def test_register():
    """Test user registration functionality"""
    url = "http://localhost:5000/auth/register"
    user_data = {
        "email": "prof@example.com",
        "password": "Password123",
        "nom": "Test",
        "prenom": "User"
    }
    
    print("\nTesting registration...")
    response = requests.post(url, json=user_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201

def test_login():
    """Test user login functionality"""
    url = "http://localhost:5000/auth/login"
    credentials = {
        "email": "prof@example.com",
        "password": "Password123"
    }
    
    print("\nTesting login...")
    response = requests.post(url, json=credentials)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def test_create_formular():
    """Test creating a new formular"""
    url = "http://localhost:5000/formulars"
    
    # Create end date (7 days from now)
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    
    formular_data = {
        "title": "Test Formular",
        "description": "This is a test formular description",
        "creator_id": 2,  # Assuming a teacher with ID 1 exists
        "end_date": end_date,
        "nb_person_group": 3
    }
    
    print("\nTesting formular creation...")
    response = requests.post(url, json=formular_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201, response.json().get('formular_id')


def test_clustering_algorithm():
    """Test the clustering algorithm with the CSV file"""
    from algo.main import main
    
    print("\nTesting clustering algorithm...")
    try:
        main()
        return True
    except Exception as e:
        print(f"Error running clustering algorithm: {e}")
        return False



if __name__ == "__main__":
    # Run the authentication tests
    test_ajout()
    #add_role("admin")
    #add_role("teacher")
    #add_role("student")
    test_prof()
    test_register()
    test_login()
    
    # Test formular functionality
    success, formular_id = test_create_formular()
    print("formulaire ")
    
    # Test clustering algorithm
    test_clustering_algorithm()
