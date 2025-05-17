from flask import Blueprint, request, jsonify
from app.utils.security import require_auth
from app.services.auth_service import update_user_password
from app.models import db, User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/profile', methods=['GET'])
@require_auth
def profile(current_user):
    return jsonify({'username': current_user.username}), 200


@user_blueprint.route('/password', methods=['PUT'])
@require_auth
def update_password(current_user):
    data = request.get_json()

    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400

    result, status_code = update_user_password(
        current_user,
        data['current_password'],
        data['new_password']
    )
    return jsonify(result), status_code
