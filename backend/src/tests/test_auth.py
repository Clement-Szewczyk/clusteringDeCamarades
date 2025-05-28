import json
import pytest

def test_register_success(client, init_database):
    """Test successful user registration."""
    response = client.post('/auth/register', json={
        'email': 'teacher@test.com',
        'password': 'Password123',
        'nom': 'Test',
        'prenom': 'Teacher'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'User registered successfully'
    assert data['user']['email'] == 'teacher@test.com'
    assert data['user']['role'] == 'teacher'

def test_register_missing_fields(client):
    """Test registration with missing fields."""
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'Password123'
        # Missing nom and prenom
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_register_invalid_email(client):
    """Test registration with invalid email format."""
    response = client.post('/auth/register', json={
        'email': 'invalid-email',
        'password': 'Password123',
        'nom': 'Test',
        'prenom': 'User'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid email format' in data['error']

def test_register_weak_password(client):
    """Test registration with weak password."""
    response = client.post('/auth/register', json={
        'email': 'teacher@test.com',
        'password': 'weak',
        'nom': 'Test',
        'prenom': 'User'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Password' in data['error']

def test_register_unauthorized_email(client):
    """Test registration with email not in student/teacher tables."""
    response = client.post('/auth/register', json={
        'email': 'unauthorized@example.com',
        'password': 'Password123',
        'nom': 'Test',
        'prenom': 'User'
    })
    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert 'not authorized' in data['error']

def test_login_success(client, init_database):
    """Test successful login."""
    # First register a user
    client.post('/auth/register', json={
        'email': 'student@test.com',
        'password': 'Password123',
        'nom': 'Test',
        'prenom': 'Student'
    })
    
    # Then login
    response = client.post('/auth/login', json={
        'email': 'student@test.com',
        'password': 'Password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'user' in data
    assert data['user']['email'] == 'student@test.com'
    assert data['user']['role'] == 'student'

def test_login_invalid_credentials(client, init_database):
    """Test login with invalid credentials."""
    response = client.post('/auth/login', json={
        'email': 'student@test.com',
        'password': 'WrongPassword123'
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid email or password' in data['error']
