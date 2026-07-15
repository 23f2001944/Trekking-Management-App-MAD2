from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import db, Role, User, TrekStatus, Trek, BookingStatus, Booking

def routes(app):
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
        role = get_jwt().get('role')
        if role not in (Role.ADMIN, Role.STAFF):
            return jsonify({'message': 'Admin or assigned staff access required'}), 401
        
        trek = Trek.query.filter_by(id=trek_id).first()
        
        if not trek:
            return jsonify({'message': "Trek doesn't exist."}), 404
        
        if role == Role.STAFF:
            staff_id = int(get_jwt_identity())
            if trek.assigned_staff_id != staff_id:
                return jsonify({'message': 'You are not assigned to this trek'}), 403
        
        if trek.status == TrekStatus.COMPLETED:
            return jsonify({'message': 'Completed treks cannot be edited'}), 400
        
        data = request.get_json(silent=True) or {}

        if role == Role.STAFF:
            allowed_fields = {'status', 'available_slots'}
            if any(key not in allowed_fields for key in data):
                return jsonify({'message': 'Staff can only update status and available_slots'}), 403

            if 'status' in data:
                if data.get('status') not in TrekStatus.ALL:
                    return jsonify({'message': 'Invalid trek status'}), 400
                trek.status = data['status']

            if 'available_slots' in data:
                new_available = data['available_slots']
                if new_available < 0:
                    return jsonify({'message': 'available_slots cannot be negative'}), 400
                if new_available > trek.total_slots:
                    return jsonify({'message': 'available_slots cannot exceed total_slots'}), 400
                trek.available_slots = new_available

            db.session.commit()
            return jsonify({'message': 'Trek updated successfully!'}), 200

        trek.name = data.get('name', trek.name)
        trek.description = data.get('description', trek.description)
        trek.location = data.get('location', trek.location)
        trek.difficulty = data.get('difficulty', trek.difficulty)

        if 'status' in data:
            if data.get('status') not in TrekStatus.ALL:
                return jsonify({'message': 'Invalid trek status'}), 400
            trek.status = data.get('status', trek.status)

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

        if new_available < 0:
            return jsonify({'message': 'available_slots cannot be negative'}), 400

        if new_available > new_total:
            return jsonify({'message': 'available_slots cannot exceed total_slots'}), 400

        occupied = trek.total_slots - trek.available_slots
        if new_total < occupied:
            return jsonify({'message': 'total_slots cannot be less than occupied slots'}), 400

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


    @app.route('/api/treks', methods=['GET'])
    @jwt_required()
    def get_treks():
        role = get_jwt().get('role')
        query = Trek.query

        # Role based filtering for differet lists
        if role == Role.TREKKER:
            query = query.filter(Trek.status.in_([TrekStatus.APPROVED, TrekStatus.OPEN])) 

        elif role == Role.STAFF:
            query = query.filter_by(assigned_staff_id = int(get_jwt_identity()))

        elif role == Role.ADMIN:
            pass    # no filter for admin

        else:
            return jsonify({'message': 'Unauthorized access'}), 401
        
        # optional filters might remove later
        location = request.args.get('location')
        difficulty = request.args.get('difficulty')

        if location:
            query = query.filter(Trek.location.ilike(f'%{location}%'))

        if difficulty:
            query = query.filter(Trek.difficulty == difficulty)

        treks = query.all()

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
                'assigned_staff_id': trek.assigned_staff_id,
                'duration': trek.duration,
            }
            data.append(trek_data)
        return jsonify(data)


    @app.route('/api/delete/trek/<int:trek_id>', methods=['DELETE'])
    @jwt_required()
    def delete_trek(trek_id):
        if get_jwt().get('role') != Role.ADMIN:
            return jsonify({'message': 'Admin access required'}), 401
        trek = Trek.query.get(trek_id)
        if not trek:
            return jsonify({'message': "Trek doesn't exist."}), 404
        if trek.bookings:  # has any bookings, cancelled or not
            return jsonify({'message': 'Cannot delete a trek with existing bookings; close it instead'}), 400
        db.session.delete(trek)
        db.session.commit()
        return jsonify({'message': 'Trek deleted successfully!'}), 200