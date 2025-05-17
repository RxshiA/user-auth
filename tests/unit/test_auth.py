import pytest
import jwt
from datetime import datetime
from app.utils.security import generate_token, verify_token


def test_token_generation_validation():
    # Mock the app context with a secret key
    secret_key = 'test-secret-key'
    user_id = 1

    # Create a token
    token = generate_token(user_id)

    # Verify it can be decoded
    decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
    assert decoded['user_id'] == user_id
    assert 'exp' in decoded
    assert 'iat' in decoded
