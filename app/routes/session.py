from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_user  # Import current_user and login_user
from app.form import LoginForm
from app.models import Employee  # Ensure you have the Employee model and LoginForm properly defined

bp = Blueprint('session', __name__, url_prefix='/session')

@bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:  # Check if the user is already logged in
        return redirect(url_for("orders.index"))  # Redirect to the orders page if authenticated
    form = LoginForm()  # Initialize the login form
    if form.validate_on_submit():
        empl_number = form.employee_number.data  # Get the employee number from the form
        employee = Employee.query.filter(Employee.employee_number == empl_number).first()  # Query the employee
        if not employee or not employee.check_password(form.password.data):  # Check if the employee exists and password matches
            return redirect(url_for(".login"))  # Redirect back to login on failure
        login_user(employee)  # Log the user in using Flask-Login
        return redirect(url_for("orders.index"))  # Redirect to the orders page
    return render_template("login.html", form=form)  # Render the login template
@bp.route('/logout', methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for('.login'))
