import json
import pytest
from datetime import datetime, timedelta

def test_get_all_formulars(client, init_database):
    """Test getting all formulars."""
    response = client.get('/formulars')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_formular_by_id(client, init_database):
    """Test getting a formular by ID."""
    # First create a formular to retrieve
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    
    create_response = client.post('/formulars', json={
        'title': 'Test Formular',
        'description': 'This is a test formular description',
        'creator_id': 1,  # Assuming a teacher with ID 1 exists
        'end_date': end_date,
        'nb_person_group': 3
    })
    assert create_response.status_code == 201
    formular_data = json.loads(create_response.data)
    formular_id = formular_data['formular_id']
    
    # Get the specific formular
    response = client.get(f'/formulars/{formular_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['formular_id'] == formular_id
    assert data['formular_title'] == 'Test Formular'
    assert data['formular_description'] == 'This is a test formular description'

def test_get_nonexistent_formular(client):
    """Test getting a formular that doesn't exist."""
    response = client.get('/formulars/9999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_create_formular(client):
    """Test creating a new formular."""
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    
    response = client.post('/formulars', json={
        'title': 'New Test Formular',
        'description': 'This is a new test formular description',
        'creator_id': 1,
        'end_date': end_date,
        'nb_person_group': 4
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['formular_title'] == 'New Test Formular'
    assert data['formular_description'] == 'This is a new test formular description'
    assert data['formular_nb_person_group'] == 4

def test_create_formular_missing_fields(client):
    """Test creating a formular with missing required fields."""
    response = client.post('/formulars', json={
        'title': 'Incomplete Formular',
        # Missing other required fields
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing required field' in data['error']

def test_update_formular(client, init_database):
    """Test updating a formular."""
    # First create a formular to update
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    
    create_response = client.post('/formulars', json={
        'title': 'Formular To Update',
        'description': 'This formular will be updated',
        'creator_id': 1,
        'end_date': end_date,
        'nb_person_group': 3
    })
    formular_data = json.loads(create_response.data)
    formular_id = formular_data['formular_id']
    
    # Update the formular
    new_end_date = (datetime.now() + timedelta(days=14)).isoformat()
    update_response = client.put(f'/formulars/{formular_id}', json={
        'title': 'Updated Formular',
        'description': 'This formular has been updated',
        'end_date': new_end_date,
        'nb_person_group': 5
    })
    assert update_response.status_code == 200
    updated_data = json.loads(update_response.data)
    assert updated_data['formular_title'] == 'Updated Formular'
    assert updated_data['formular_description'] == 'This formular has been updated'
    assert updated_data['formular_nb_person_group'] == 5

def test_delete_formular(client):
    """Test deleting a formular."""
    # First create a formular to delete
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    
    create_response = client.post('/formulars', json={
        'title': 'Formular To Delete',
        'description': 'This formular will be deleted',
        'creator_id': 1,
        'end_date': end_date,
        'nb_person_group': 2
    })
    formular_data = json.loads(create_response.data)
    formular_id = formular_data['formular_id']
    
    # Delete the formular
    delete_response = client.delete(f'/formulars/{formular_id}')
    assert delete_response.status_code == 204
    
    # Verify formular is gone
    get_response = client.get(f'/formulars/{formular_id}')
    assert get_response.status_code == 404

def test_get_teacher_formulars(client, init_database):
    """Test getting all formulars created by a specific teacher."""
    # First create some formulars for the teacher
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    teacher_id = 1  # Assuming a teacher with ID 1 exists
    
    # Create two formulars for this teacher
    client.post('/formulars', json={
        'title': 'Teacher Formular 1',
        'description': 'First formular by teacher',
        'creator_id': teacher_id,
        'end_date': end_date,
        'nb_person_group': 3
    })
    
    client.post('/formulars', json={
        'title': 'Teacher Formular 2',
        'description': 'Second formular by teacher',
        'creator_id': teacher_id,
        'end_date': end_date,
        'nb_person_group': 4
    })
    
    # Get all formulars for this teacher
    response = client.get(f'/teachers/{teacher_id}/formulars')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # Verify the formulars belong to this teacher
    teacher_formulars = [f for f in data if f['formular_creator'] == teacher_id]
    assert len(teacher_formulars) >= 2
