from flask import jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import db, Role, User, TrekStatus, Trek, BookingStatus, Booking

def routes(app):
    @app.route('/api/book/trek/<int:trek_id>', methods=['POST'])
    @jwt_required()
    def book_trek(trek_id):
        if get_jwt().get('role') != Role.TREKKER:
            return jsonify({'message': 'Only trekkers can book treks'}), 401

        user_id = get_jwt_identity()

        trek = Trek.query.filter_by(id=trek_id).first()
        if not trek:
            return jsonify({'message': "Trek doesn't exist."}), 404

        if trek.status != TrekStatus.OPEN:
            return jsonify({'message': 'Trek is not open for booking'}), 400

        if trek.available_slots <= 0:
            return jsonify({'message': 'No slots available for this trek'}), 400

        # for checking if the user has already booked the same trek
        existing = Booking.query.filter_by(user_id=user_id, trek_id=trek_id, status=BookingStatus.BOOKED).first()
        if existing:
            return jsonify({'message': 'You have already booked this trek'}), 400

        booking = Booking(user_id=user_id, trek_id=trek_id)
        trek.available_slots -= 1

        db.session.add(booking)
        db.session.commit()
        return jsonify({'message': 'Trek booked successfully!'}), 201


    @app.route('/api/bookings', methods=['GET'])
    @jwt_required()
    def bookings():
        role = get_jwt().get('role')

        if role == Role.TREKKER:
            user_id = int(get_jwt_identity())
            bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()

        elif role == Role.ADMIN:
            bookings = Booking.query.order_by(Booking.booking_date.desc()).all()

        else:
            return jsonify({'message': 'Unauthorized'}), 403

        data = []

        for booking in bookings:
            booking_data = {
                'id': booking.id,
                'user_id': booking.user_id,
                'trek_id': booking.trek_id,
                'trek_name': booking.trek.name,
                'location': booking.trek.location,
                'status': booking.status,
                'booking_date': booking.booking_date.strftime("%d-%m-%Y %H:%M"),
                'start_date': booking.trek.start_date.strftime("%d-%m-%Y"),
                'end_date': booking.trek.end_date.strftime("%d-%m-%Y"),
            }

            # Only admins need user details
            if role == Role.ADMIN:
                booking_data['user_name'] = booking.user.name
                booking_data['user_email'] = booking.user.email

            data.append(booking_data)

        return jsonify(data), 200


    @app.route('/api/cancel/booking/<int:booking_id>', methods=['PUT'])
    @jwt_required()
    def cancel_booking(booking_id):
        user_id = int(get_jwt_identity())
        booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()

        if not booking:
            return jsonify({'message': "Booking doesn't exist."}), 404
        if booking.status != BookingStatus.BOOKED:
            return jsonify({'message': 'Only active bookings can be cancelled'}), 400

        booking.status = BookingStatus.CANCELLED
        booking.trek.available_slots += 1
        db.session.commit()
        return jsonify({'message': 'Booking cancelled successfully!'}), 200


    @app.route('/api/user/profile', methods=['GET'])
    @jwt_required()
    def get_profile():
        user = User.query.get(int(get_jwt_identity()))
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'phone': user.phone})


    @app.route('/api/user/profile', methods=['PUT'])
    @jwt_required()
    def update_profile():
        user = User.query.get(int(get_jwt_identity()))
        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json(silent=True) or {}
        user.name = data.get('name', user.name)
        user.phone = data.get('phone', user.phone)

        if data.get('email') and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'message': 'Email already in use'}), 400
            user.email = data['email']

        if data.get('password'):
            user.password_hash = generate_password_hash(data['password'])

        db.session.commit()
        return jsonify({'message': 'Profile updated successfully!'}), 200