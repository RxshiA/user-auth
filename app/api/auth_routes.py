from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, authenticate_user
from app import limiter

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    result, status_code = register_user(data['username'], data['password'])
    return jsonify(result), status_code


@auth_blueprint.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    result, status_code = authenticate_user(data['username'], data['password'])
    return jsonify(result), status_code
