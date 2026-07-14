from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError
from models import db, Role, User, TrekStatus, Trek, BookingStatus, Booking


# single helper function to be used by both user to register for himself, and by the admin to register new staff members
def create_user(data, role):
    required = ['name', 'email', 'password']
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({'message': f'Missing fields: {", ".join(missing)}'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists!'}), 400

    user = User(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        password_hash=generate_password_hash(data['password']),
        role=role
    )
    db.session.add(user)

    try:        # to prevent race condition where two users try to register with the same email at the same time
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User already exists!'}), 400

    return jsonify({'message': 'User registered successfully!'}), 201

def routes(app):
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json(silent=True) or {}
        return create_user(data, Role.TREKKER)

    @app.route('/api/admin/create-staff', methods=['POST'])
    @jwt_required()
    def create_staff():
        if get_jwt().get('role') != Role.ADMIN:
            return jsonify({'message': 'Admin access required'}), 401

        data = request.get_json(silent=True) or {}
        return create_user(data, Role.STAFF)


    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json(silent=True) or {}
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and Password are required!'}), 400 
        
        user = User.query.filter_by(email=data['email']).first()
        if user and user.is_active and check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=str(user.id), additional_claims={'role':user.role})
            return jsonify({'message': 'Login successful!', 'data': {'name': user.name, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
        else:
            return jsonify({'message': 'Invalid credentials or user blacklisted!'}), 400  