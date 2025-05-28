import requests

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
        "email": "test@example.com",
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
        "email": "test@example.com",
        "password": "Password123"
    }
    
    print("\nTesting login...")
    response = requests.post(url, json=credentials)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

if __name__ == "__main__":
    # Run the authentication tests
    #test_ajout()
    #add_role("admin")
    #add_role("teacher")
    #add_role("student")
    #test_register()
    test_login()