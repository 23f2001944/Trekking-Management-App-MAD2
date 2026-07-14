from flask import Flask, jsonify, request
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import db, Role, User, TrekStatus, Trek, BookingStatus, Booking

def routes(app):
    @app.route('/api/admin/users', methods=['GET'])
    @jwt_required()
    def get_users():
        if get_jwt().get('role') != Role.ADMIN:
            return jsonify({'message': 'Admin access required'}), 401

        query = User.query.filter(User.role != Role.ADMIN)

        role_filter = request.args.get('role')
        search = request.args.get('search')
        if role_filter:
            query = query.filter_by(role=role_filter)
        if search:
            query = query.filter(or_(User.name.ilike(f'%{search}%'), User.email.ilike(f'%{search}%')))

        users = query.all()

        data = []
        for user in users:
            user_data = {
                'id': user.id, 
                'name': user.name, 
                'email': user.email, 
                'phone': user.phone,
                'role': user.role, 
                'is_active': user.is_active
            }
            data.append(user_data)
        return jsonify(data)

    @app.route('/api/admin/user/<int:user_id>/status', methods=['PUT'])
    @jwt_required()
    def update_user_status(user_id):
        if get_jwt().get('role') != Role.ADMIN:
            return jsonify({'message': 'Admin access required'}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        if user.role == Role.ADMIN:
            return jsonify({'message': 'Cannot deactivate the admin account'}), 400

        data = request.get_json(silent=True) or {}
        if 'is_active' not in data:
            return jsonify({'message': 'is_active is required'}), 400

        user.is_active = bool(data['is_active'])
        db.session.commit()
        return jsonify({'message': 'User status updated successfully!'}), 200


    @app.route('/api/dashboard/stats', methods=['GET'])
    @jwt_required()
    def dashboard_stats():
        role = get_jwt().get('role')

        if role == Role.ADMIN:
            return jsonify({
                'total_treks': Trek.query.count(),
                'total_users': User.query.filter_by(role=Role.TREKKER).count(),
                'total_staff': User.query.filter_by(role=Role.STAFF).count(),
                'total_bookings': Booking.query.filter_by(status=BookingStatus.BOOKED).count()
            })

        elif role == Role.STAFF:
            staff_id = int(get_jwt_identity())

            assigned_treks = Trek.query.filter_by(assigned_staff_id=staff_id).count()

            # works because every trekker can book a trek only once
            total_participants = Booking.query.join(Trek).filter(Trek.assigned_staff_id == staff_id,Booking.status == BookingStatus.BOOKED).count()

            ongoing_treks = Trek.query.filter_by(assigned_staff_id=staff_id,status=TrekStatus.OPEN).count()

            return jsonify({
                'assigned_treks': assigned_treks,
                'total_participants': total_participants,
                'ongoing_treks': ongoing_treks
            })
        
        return jsonify({'message': 'Unauthorized'}), 403