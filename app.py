from flask import Flask, request, jsonify
from models import db, User
from auth import generate_token, verify_token
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

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

if __name__ == '__main__':
    app.run(debug=True)