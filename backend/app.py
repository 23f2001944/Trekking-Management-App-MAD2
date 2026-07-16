from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
from models import db, cache, Role, User

from routes.auth import routes as auth_routes
from routes.admin import routes as admin_routes
from routes.trek import routes as trek_routes
from routes.user import routes as user_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = os.getenv('REDIS_HOST', 'localhost')
app.config['CACHE_REDIS_PORT'] = int(os.getenv('REDIS_PORT', 6379))
app.config['CACHE_REDIS_DB'] = int(os.getenv('CACHE_REDIS_DB', 0))
app.config['CACHE_DEFAULT_TIMEOUT'] = 60    # in seconds

CORS(app)

db.init_app(app)
cache.init_app(app)

jwt = JWTManager(app)

auth_routes(app)
admin_routes(app)
trek_routes(app)
user_routes(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Creates the admin when the app is run for the first time
        if not User.query.filter_by(name='admin').first():
            admin = User(name="admin", email="admin@local.com", password_hash=generate_password_hash('Admin@123'), role=Role.ADMIN)
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)