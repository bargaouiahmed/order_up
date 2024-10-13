from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
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


class Table(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))
    finished = db.Column(db.Boolean, nullable=False)

    # Add relationship to order details (the items in this order)
    details = db.relationship('OrderDetails', backref='order', lazy=True)
    employee = db.relationship('Employee', backref='orders')  # Relationship to Employee



class MenuItemType(db.Model):
    __tablename__ = 'menu_item_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    # One-to-many relationship with MenuItem
    items = db.relationship('MenuItem', backref='type', lazy=True)


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Foreign keys to Menu and MenuItemType
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    menu_type_id = db.Column(db.Integer, db.ForeignKey('menu_item_types.id'), nullable=False)


class OrderDetails(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
