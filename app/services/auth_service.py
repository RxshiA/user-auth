from werkzeug.security import generate_password_hash
from app.models import db, User
from app.utils.security import generate_token


def register_user(username, password):
    """Register a new user"""
    if User.query.filter_by(username=username).first():
        return {'error': 'User already exists'}, 400

    if len(password) < 8:
        return {'error': 'Password must be at least 8 characters'}, 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return {'message': 'User registered successfully'}, 201


def authenticate_user(username, password):
    """Authenticate a user and return a token"""
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        token = generate_token(user.id)
        return {'token': token}, 200

    return {'error': 'Invalid credentials'}, 401


def update_user_password(user, current_password, new_password):
    """Update a user's password"""
    if not user.check_password(current_password):
        return {'error': 'Current password is incorrect'}, 401

    if len(new_password) < 8:
        return {'error': 'New password must be at least 8 characters'}, 400

    user.password_hash = generate_password_hash(
        new_password, method='pbkdf2:sha256:600000')
    db.session.commit()

    return {'message': 'Password updated successfully'}, 200
