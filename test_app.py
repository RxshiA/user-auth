import pytest
from app import app, db
from models import User

# ---------- Setup ----------

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Optional if using forms
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # Cleanup
        with app.app_context():
            db.session.remove()
            db.drop_all()

# ---------- Test Cases ----------


def test_register_duplicate_username(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'User already exists'


def test_login_success(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


def test_profile_access_with_token(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    login_res = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = login_res.get_json()['token']

    profile_res = client.get('/profile', headers={'Authorization': f'Bearer {token}'})
    assert profile_res.status_code == 200
    assert profile_res.get_json()['username'] == 'testuser'
