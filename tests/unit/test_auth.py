import jwt
from flask import current_app
from app.utils.security import generate_token


def test_token_generation_validation(app):
    with app.app_context():
        secret_key = current_app.config['SECRET_KEY']
        user_id = 1

        token = generate_token(user_id)

        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        assert decoded['user_id'] == user_id
        assert 'exp' in decoded
        assert 'iat' in decoded
