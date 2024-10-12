from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'  # Define the table name

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Name, not nullable
    employee_number = db.Column(db.Integer, nullable=False, unique=True)  # Unique employee number, not nullable
    hashed_password = db.Column(db.String(255), nullable=False)  # Hashed password, not nullable

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
