from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from models import db, Role, User, TrekStatus, Trek, BookingStatus, Booking

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tma-mad2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'thisismysecretkeyfornow'

CORS(app)

db.init_app(app)

jwt = JWTManager(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists!'}), 400    
    user = User(
        name = data['name'],
        email = data['email'],
        phone = data['phone'],
        password_hash = generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.is_active and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id, additional_claims={'role':user.role})
        return jsonify({'message': 'Login successful!', 'data': {'name': user.name, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid credentials or user blacklisted!'}), 400  
    

@app.route('/api/create/trek', methods=['POST'])
@jwt_required()
def create_trek():
    if get_jwt().get('role') != Role.ADMIN:
        return jsonify({'message': 'Admin access required'}), 401
    
    data = request.get_json()
    trek = (
        
    )


@app.route('/api/get/trekdata', methods=['GET'])
@jwt_required()
def get_trekdata():
    if get_jwt().get('role') != Role.ADMIN:
        return jsonify({'message': 'Admin access required'}), 401

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Creates the admin when the app is run for the first time
        if not User.query.filter_by(name='admin').first():
            admin = User(name="admin", email="admin@local.com", password_hash=generate_password_hash('Admin@123'), role=Role.ADMIN)
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)