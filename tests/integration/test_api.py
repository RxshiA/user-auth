import pytest
import json
from app.utils.security import generate_token


def test_register_user(client):
    response = client.post(
        '/auth/register',
        data=json.dumps({'username': 'newuser', 'password': 'password123'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'User registered successfully'


def test_login_success(client, test_user):
    response = client.post(
        '/auth/login',
        data=json.dumps({'username': 'testuser', 'password': 'password123'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data


def test_profile_access(client, test_user, app):
    with app.app_context():
        token = generate_token(test_user.id)

    response = client.get(
        '/users/profile',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'testuser'
