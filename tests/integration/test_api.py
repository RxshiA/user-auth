import json


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
