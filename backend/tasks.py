import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, timedelta
from celery_app import celery

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'youremail@gmail.com'
SMTP_PASSWORD = 'your-16-char-app-password' 

EXPORT_DIR = os.path.join(os.path.dirname(__file__), 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)

def send_email(to_email, subject, html_body):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.attach(MIMEText(html_body, 'html'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())

@celery.task
def send_daily_reminders():
    # imported here (not at top) to dodge a circular import with app.py
    from app import app
    from models import Trek, Booking, BookingStatus, TrekStatus

    with app.app_context():
        tomorrow = date.today() + timedelta(days=1)
        treks = Trek.query.filter_by(start_date=tomorrow, status=TrekStatus.OPEN).all()

        sent_count = 0
        for trek in treks:
            bookings = Booking.query.filter_by(trek_id=trek.id, status=BookingStatus.BOOKED).all()
            for booking in bookings:
                user = booking.user
                html = f"""
                <h3>Trek Reminder</h3>
                <p>Hi {user.name},</p>
                <p>Your trek <b>{trek.name}</b> starts tomorrow ({trek.start_date.strftime('%d-%m-%Y')}).</p>
                <p>Location: {trek.location}<br>Difficulty: {trek.difficulty}</p>
                <p>Please be ready on time. Happy trekking!</p>
                """
                send_email(user.email, f"Reminder: {trek.name} starts tomorrow", html)
                sent_count += 1
        return f"Sent {sent_count} reminders"
    
@celery.task
def send_monthly_report():
    from app import app
    from models import Trek, Booking, User, Role, BookingStatus, TrekStatus
    from sqlalchemy import func

    with app.app_context():
        today = date.today()
        first_of_this_month = today.replace(day=1)
        last_month_end = first_of_this_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        treks_conducted = Trek.query.filter(
            Trek.status == TrekStatus.COMPLETED,
            Trek.end_date >= last_month_start,
            Trek.end_date <= last_month_end
        ).count()

        participant_count = (Booking.query.join(Trek)
            .filter(Trek.end_date >= last_month_start, Trek.end_date <= last_month_end)
            .filter(Booking.status.in_([BookingStatus.BOOKED, BookingStatus.COMPLETED]))
            .count())

        popular = (Booking.query.join(Trek)
            .filter(Trek.end_date >= last_month_start, Trek.end_date <= last_month_end)
            .with_entities(Trek.name, func.count(Booking.id).label('cnt'))
            .group_by(Trek.name)
            .order_by(func.count(Booking.id).desc())
            .limit(5).all())

        rows = "".join(f"<tr><td>{name}</td><td>{cnt}</td></tr>" for name, cnt in popular) or "<tr><td colspan='2'>No bookings</td></tr>"

        html = f"""
        <h2>Monthly Trekking Report - {last_month_start.strftime('%B %Y')}</h2>
        <p>Total treks completed: {treks_conducted}</p>
        <p>Total participants: {participant_count}</p>
        <h4>Popular Treks</h4>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr><th>Trek Name</th><th>Bookings</th></tr>
          {rows}
        </table>
        """

        admin = User.query.filter_by(role=Role.ADMIN).first()
        send_email(admin.email, f"Monthly Trekking Report - {last_month_start.strftime('%B %Y')}", html)
        return "Report sent"

@celery.task(bind=True)
def export_booking_history(self, user_id):
    from app import app
    from models import Booking

    with app.app_context():
        bookings = (Booking.query.filter_by(user_id=user_id)
                    .order_by(Booking.booking_date.desc()).all())

        filename = f"history_{user_id}_{self.request.id}.csv"
        filepath = os.path.join(EXPORT_DIR, filename)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['User ID', 'Trek Name', 'Location', 'Booking Status', 'Start Date', 'End Date'])
            for b in bookings:
                writer.writerow([
                    b.user_id,
                    b.trek.name,
                    b.trek.location,
                    b.status,
                    b.trek.start_date.strftime('%d-%m-%Y'),
                    b.trek.end_date.strftime('%d-%m-%Y')
                ])

        return filename