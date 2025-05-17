from flask import Flask, request, jsonify
from models import db, User
from auth import generate_token, verify_token
from config import Config
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config.from_object(Config)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def health():
    return 'OK', 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_token(user.id)
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/profile', methods=['GET'])
def profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Token is missing'}), 401

    token = auth_header.split(" ")[1]
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

    user = User.query.get(user_id)
    return jsonify({'username': user.username}), 200


@app.route('/update-password', methods=['PUT'])
def update_password():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Token is missing'}), 401

    if " " in auth_header:
        token = auth_header.split(" ")[1]
    else:
        token = auth_header 

    user_id = verify_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

    data = request.get_json()
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    user.password_hash = generate_password_hash(data['new_password'])
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
