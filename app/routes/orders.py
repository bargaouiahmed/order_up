from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Employee, Table
from app import db

bp = Blueprint("orders", __name__, url_prefix="")

@bp.route("/")
@login_required
def index():
    tables = Table.query.all()  # Retrieves all table records
    servers = Employee.query.all()
    return render_template('orders.html', title="Welcome to Order Up", tables=tables, servers=servers)
