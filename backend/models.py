from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Role:
    ADMIN = "admin"
    STAFF = "staff"
    TREKKER = "trekker"
    ALL = (ADMIN, STAFF, TREKKER)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Role.TREKKER)
    phone = db.Column(db.String(20))
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrekStatus:
    PENDING = "Pending"
    APPROVED = "Approved"
    OPEN = "Open"
    CLOSED = "Closed"
    COMPLETED = "Completed"
    ALL = (PENDING, APPROVED, OPEN, CLOSED, COMPLETED)

class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)   # Easy / Moderate / Hard
    status = db.Column(db.String(20), nullable=False, default=TrekStatus.PENDING)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    staff = db.relationship( "User", foreign_keys=[assigned_staff_id],backref="assigned_treks")

    # Calculated property (NOT stored in DB)
    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

class BookingStatus:
    BOOKED = "Booked"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    ALL = (BOOKED, CANCELLED, COMPLETED)

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column( db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id], backref="bookings")

    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    trek = db.relationship("Trek", foreign_keys=[trek_id], backref="bookings")

    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=BookingStatus.BOOKED)

    # payment_status = db.Column(db.String(20), default="Pending")  # Optional for later