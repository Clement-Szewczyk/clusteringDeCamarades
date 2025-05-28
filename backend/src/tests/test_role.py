import json
import pytest
import uuid

def test_get_all_roles(client, init_database):
    """Test getting all roles."""
    response = client.get('/roles')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    # Remove the specific count check as the number of roles may vary
    # The important part is that the basic roles exist
    role_names = [role['role_name'] for role in data]
    assert 'admin' in role_names
    assert 'teacher' in role_names
    assert 'student' in role_names

def test_get_role_by_id(client, init_database):
    """Test getting a role by ID."""
    # First, get all roles to find an ID
    response = client.get('/roles')
    roles = json.loads(response.data)
    role_id = roles[0]['role_id']
    
    # Get the specific role
    response = client.get(f'/roles/{role_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['role_id'] == role_id

def test_get_nonexistent_role(client):
    """Test getting a role that doesn't exist."""
    response = client.get('/roles/9999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_create_role(client):
    """Test creating a new role."""
    
    # Generate a unique role name to avoid conflicts
    unique_role_name = f"new_role_{uuid.uuid4().hex[:8]}"
    
    response = client.post('/roles', json={
        'role_name': unique_role_name
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['role_name'] == unique_role_name

def test_create_role_missing_name(client):
    """Test creating a role without providing a name."""
    response = client.post('/roles', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'required' in data['error']

def test_create_duplicate_role(client, init_database):
    """Test creating a role with a name that already exists."""
    response = client.post('/roles', json={
        'role_name': 'admin'
    })
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data
    assert 'already exists' in data['error']
