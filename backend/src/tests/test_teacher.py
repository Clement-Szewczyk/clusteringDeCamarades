import json
import pytest

def test_get_all_teachers(client, init_database):
    """Test getting all teachers."""
    response = client.get('/teachers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['teacher_email'] == 'teacher@test.com'

def test_get_teacher_by_email(client, init_database):
    """Test getting a teacher by email."""
    response = client.get('/teachers/teacher@test.com')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['teacher_email'] == 'teacher@test.com'

def test_get_nonexistent_teacher(client):
    """Test getting a teacher that doesn't exist."""
    response = client.get('/teachers/nonexistent@test.com')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_create_teacher(client):
    """Test creating a new teacher."""
    response = client.post('/teachers', json={
        'email': 'new_teacher@test.com'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['teacher_email'] == 'new_teacher@test.com'

def test_create_teacher_invalid_email(client):
    """Test creating a teacher with invalid email."""
    response = client.post('/teachers', json={
        'email': 'invalid-email'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid email format' in data['error']

def test_create_duplicate_teacher(client, init_database):
    """Test creating a teacher with an email that already exists."""
    response = client.post('/teachers', json={
        'email': 'teacher@test.com'
    })
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data
    assert 'already exists' in data['error']

def test_create_teachers_batch(client):
    """Test creating multiple teachers in a batch."""
    response = client.post('/teachers/batch', json=[
        {'email': 'batch_teacher1@test.com'},
        {'email': 'batch_teacher2@test.com'},
        {'email': 'invalid-email'}  # This one should fail
    ])
    assert response.status_code == 207  # Multi-Status
    data = json.loads(response.data)
    assert 'success' in data
    assert 'failed' in data
    assert len(data['success']) == 2
    assert len(data['failed']) == 1

def test_update_teacher(client, init_database):
    """Test updating a teacher."""
    # Update the teacher
    response = client.put('/teachers/teacher@test.com', json={
        'email': 'updated_teacher@test.com'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['teacher_email'] == 'updated_teacher@test.com'

def test_delete_teacher(client, init_database):
    """Test deleting a teacher."""
    # First, create a teacher to delete
    response = client.post('/teachers', json={
        'email': 'to_delete@test.com'
    })
    
    # Delete the teacher
    response = client.delete('/teachers/to_delete@test.com')
    assert response.status_code == 204
    
    # Verify teacher is gone
    response = client.get('/teachers/to_delete@test.com')
    assert response.status_code == 404
