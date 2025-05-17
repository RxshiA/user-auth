import pytest
from app import create_app
from app.models import db, User


@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a test user for the tests."""
    with app.app_context():
        user = User(username='testuser', password='password123')
        db.session.add(user)
        db.session.commit()
        return user
