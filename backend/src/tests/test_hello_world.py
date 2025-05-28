import json
import pytest

def test_get_hello_world(client):
    """Test getting the default hello world message."""
    response = client.get('/hello')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Hello, World!'

def test_create_hello_world(client):
    """Test creating a custom hello world message."""
    response = client.post('/hello', json={
        'message': 'Custom Hello!'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Custom Hello!'

def test_create_hello_world_no_message(client):
    """Test creating a hello world message without specifying one."""
    response = client.post('/hello', json={})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Hello, World!'  # Should use default
