from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from datetime import datetime
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
    data = request.get_json(silent=True) or {}      # if there is no data empty {} is passed
    required = ['name', 'email', 'password']
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({'message': f'Missing fields: {", ".join(missing)}'}), 400 

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists!'}), 400    
    
    user = User(
        name = data['name'],
        email = data['email'],
        phone = data.get('phone'),
        password_hash = generate_password_hash(data['password'])
    )
    db.session.add(user)
    try:        # to prevent race condition where two users try to register using same email at the same time
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User already exists!'}), 400
    
    return jsonify({'message': 'User registered successfully!'}), 201


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
    

@app.route('/api/create/trek', methods=['POST'])
@jwt_required()
def create_trek():
    if get_jwt().get('role') != Role.ADMIN:
        return jsonify({'message': 'Admin access required'}), 401
    
    data = request.get_json(silent=True) or {}
    required = ['name', 'location', 'difficulty', 'start_date', 'end_date', 'total_slots']
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({'message': f'Missing fields: {", ".join(missing)}'}), 400 
    
    try:
        start = datetime.strptime(data["start_date"], "%d-%m-%Y").date()
        end = datetime.strptime(data["end_date"], "%d-%m-%Y").date()
    except ValueError:
        return jsonify({'message': 'Dates must be in DD-MM-YYYY format'}), 400
    
    if start >= end:
        return jsonify({'message': 'start_date must be before end_date'}), 400

    assigned_staff_id = data.get('assigned_staff_id')
    if assigned_staff_id is not None:
        staff = User.query.filter_by(id=assigned_staff_id, role=Role.STAFF, is_active=True).first()
        if not staff:
            return jsonify({'message': 'assigned_staff_id must belong to an active staff member'}), 400

    trek = Trek(
        name = data['name'],
        description = data.get('description'),
        location = data['location'],
        difficulty = data['difficulty'],
        start_date = start,
        end_date = end,
        total_slots = data['total_slots'],
        available_slots = data['total_slots'],
        assigned_staff_id = assigned_staff_id
    )
    db.session.add(trek)
    db.session.commit()   
    return jsonify({'message': 'Trek created successfully!'}), 201

@app.route('/api/update/trek/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    if get_jwt().get('role') != Role.ADMIN:
        return jsonify({'message': 'Admin access required'}), 401
    
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trek:
        return jsonify({'message': "Trek doesn't exist."}), 401
    
    data = request.get_json(silent=True) or {}
    trek.name = data.get('name', trek.name)
    trek.description = data.get('description', trek.description)
    trek.location = data.get('location', trek.location)
    trek.difficulty = data.get('difficulty', trek.difficulty)

    if data.get('start_date') or data.get('end_date'):
        try:
            if data.get('start_date'):
                trek.start_date = datetime.strptime(data['start_date'], "%d-%m-%Y").date()

            if data.get('end_date'):
                trek.end_date = datetime.strptime(data['end_date'], "%d-%m-%Y").date()

        except ValueError:
            return jsonify({ 'message': 'Dates must be in DD-MM-YYYY format'}), 400

    if trek.start_date >= trek.end_date:
        return jsonify({'message': 'start_date must be before end_date'}), 400

    new_total = data.get('total_slots', trek.total_slots)
    new_available = data.get('available_slots', trek.available_slots)

    if new_available > new_total:
        return jsonify({
            'message': 'available_slots cannot exceed total_slots'
        }), 400

    occupied = trek.total_slots - trek.available_slots
    if new_total < occupied:
        return jsonify({
            'message': 'total_slots cannot be less than occupied slots'
        }), 400

    trek.total_slots = new_total
    trek.available_slots = new_available
    
    if 'assigned_staff_id' in data:
        new_staff_id = data['assigned_staff_id']
        if new_staff_id is not None:
            staff = User.query.filter_by(id=new_staff_id, role=Role.STAFF, is_active=True).first()
            if not staff:
                return jsonify({'message': 'assigned_staff_id must belong to an active staff member'}), 400
        trek.assigned_staff_id = new_staff_id

    db.session.commit()
    return jsonify({'message': 'Trek updated successfully!'}), 201


@app.route('/api/get/treks', methods=['GET'])
@jwt_required()
def get_treks():
    if get_jwt().get('role') != Role.ADMIN:
        return jsonify({'message': 'Admin access required'}), 401

    treks = Trek.query.all()

    data = []
    for trek in treks:
        trek_data = {
            'id' : trek.id,
            'name' : trek.name,
            'description' : trek.description,
            'location' : trek.location,
            'difficulty' : trek.difficulty,
            'status' : trek.status,
            'start_date' : trek.start_date.strftime("%d-%m-%Y"),
            'end_date' : trek.end_date.strftime("%d-%m-%Y"),
            'total_slots' : trek.total_slots,
            'available_slots' : trek.available_slots,
            'assigned_staff_id': trek.assigned_staff_id
        }
        data.append(trek_data)
    return jsonify(data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Creates the admin when the app is run for the first time
        if not User.query.filter_by(name='admin').first():
            admin = User(name="admin", email="admin@local.com", password_hash=generate_password_hash('Admin@123'), role=Role.ADMIN)
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)