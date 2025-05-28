import json
import pytest

def test_get_all_votes(client, init_database):
    """Test getting all votes."""
    response = client.get('/votes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_vote_by_id(client, init_database):
    """Test getting a vote by ID."""
    # First, create a vote to retrieve
    new_vote_response = client.post('/votes', json={
        'userid': 1,
        'idform': 1,
        'idstudent': 1,
        'weight': 5
    })
    assert new_vote_response.status_code == 201
    vote_id = json.loads(new_vote_response.data)['vote_idvote']
    
    # Now retrieve the vote
    response = client.get(f'/votes/{vote_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['vote_idvote'] == vote_id
    assert data['vote_userid'] == 1
    assert data['vote_formid'] == 1
    assert data['vote_studentid'] == 1
    assert data['weigth'] == 5

def test_get_nonexistent_vote(client):
    """Test getting a vote that doesn't exist."""
    response = client.get('/votes/9999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_create_vote(client):
    """Test creating a new vote."""
    response = client.post('/votes', json={
        'userid': 1,
        'idform': 1,
        'idstudent': 2,
        'weight': 10
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['vote_userid'] == 1
    assert data['vote_formid'] == 1
    assert data['vote_studentid'] == 2
    assert data['weigth'] == 10

def test_create_vote_missing_fields(client):
    """Test creating a vote with missing required fields."""
    response = client.post('/votes', json={
        'userid': 1,
        'idform': 1
        # Missing studentid and weight
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing required field' in data['error']

def test_get_votes_by_user(client, init_database):
    """Test getting all votes made by a specific user."""
    # Create a vote for user with ID 1
    client.post('/votes', json={
        'userid': 1,
        'idform': 1,
        'idstudent': 3,
        'weight': 15
    })
    
    # Get all votes for user 1
    response = client.get('/users/1/votes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(vote['vote_userid'] == 1 for vote in data)

def test_get_votes_by_form(client, init_database):
    """Test getting all votes for a specific form."""
    # Create a vote for form with ID 1
    client.post('/votes', json={
        'userid': 2,
        'idform': 1,
        'idstudent': 4,
        'weight': 20
    })
    
    # Get all votes for form 1
    response = client.get('/formulars/1/votes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(vote['vote_formid'] == 1 for vote in data)

def test_delete_vote(client, init_database):
    """Test deleting a vote by ID."""
    # First, create a vote to delete
    new_vote_response = client.post('/votes', json={
        'userid': 3,
        'idform': 2,
        'idstudent': 5,
        'weight': 25
    })
    vote_id = json.loads(new_vote_response.data)['vote_idvote']
    
    # Delete the vote
    response = client.delete(f'/votes/{vote_id}')
    assert response.status_code == 204
    
    # Verify vote is gone
    get_response = client.get(f'/votes/{vote_id}')
    assert get_response.status_code == 404

def test_delete_nonexistent_vote(client):
    """Test deleting a vote that doesn't exist."""
    response = client.delete('/votes/9999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
