from flask import Flask
from .config import Configuration
from .models import db, Employee
from .routes import orders, session
from flask_login import LoginManager
import os

# Initialize the app and database
app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)

# Initialize Flask-Login
login = LoginManager(app)
login.login_view = "session.login"

# Register Blueprints
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))

# Ensure database is created at the start of the application
with app.app_context():
    db.create_all()
