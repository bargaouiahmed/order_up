from dotenv import load_dotenv
load_dotenv()

from app import app, db
from app.models import Employee, Menu, MenuItem, MenuItemType, Table  # Import the new models

with app.app_context():
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()

    # Create an employee
    employee = Employee(name="Margot", employee_number="1234", password='password')
    db.session.add(employee)

    # Create MenuItemType instances
    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    # Add them to the session
    db.session.add(beverages)
    db.session.add(entrees)
    db.session.add(sides)

    # Create a Menu instance
    dinner = Menu(name="Dinner")
    db.session.add(dinner)

    # Create MenuItem instances and link them to Menu and MenuItemType
    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    # Add MenuItems to the session
    db.session.add(fries)
    db.session.add(drp)
    db.session.add(jambalaya)
    for i in range(10):
        table=Table(number=i,capacity=5)
        db.session.add(table)
    # Commit all changes to the database
    db.session.commit()
