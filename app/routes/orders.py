from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Table, Order, MenuItem, OrderDetails
from app.forms import AssignTableForm
from app import db

bp = Blueprint("orders", __name__, url_prefix="")

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    tables = Table.query.all()  # Retrieve all table records
    servers = Employee.query.all()
    orders = Order.query.filter_by(finished=False).all()  # Only show open orders

    # Calculate the price for each order
    order_prices = {}
    for order in orders:
        total_price = 0
        for detail in order.details:
            menu_item = MenuItem.query.get(detail.item_id)
            total_price += menu_item.price
        order_prices[order.id] = total_price

    if request.method == "POST":
        # Handle table assignment
        table_number = request.form.get("table_number")
        server_name = request.form.get("server_name")
        if server_name and table_number:
            table = Table.query.filter_by(number=table_number).first()
            server = Employee.query.filter_by(name=server_name).first()
        if not server_name or not table_number:
            return redirect(url_for("orders.index"))
        if not table or not server:
            flash("Invalid table or server selection.")
        else:
            # Check if there is already an open order for this table
            existing_order = Order.query.filter_by(table_id=table.id, finished=False).first()
            if existing_order:
                flash(f"Table {table.number} already has an open order!")
            else:
                new_order = Order(table_id=table.id, employee_id=server.id, finished=False)
                db.session.add(new_order)
                db.session.commit()
                flash(f"Assigned Table {table.number} to {server.name}.")

        return redirect(url_for("orders.index"))

    return render_template('orders.html', title="Welcome to Order Up", tables=tables, servers=servers, orders=orders, order_prices=order_prices)


@bp.route("/close_order/<int:order_id>", methods=["POST"])
@login_required
def close_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order.finished = True
        db.session.commit()
        flash(f"Order for Table {order.table_id} closed.")
    return redirect(url_for("orders.index"))


@bp.route("/add_to_order/<int:order_id>", methods=["POST"])
@login_required
def add_to_order(order_id):
    order = Order.query.get(order_id)
    if order:
        # Assuming form contains a `menu_item_id` to add an item to the order
        menu_item_id = request.form.get("menu_item_id")
        menu_item = MenuItem.query.get(menu_item_id)
        if menu_item:
            order_detail = OrderDetails(order_id=order.id, item_id=menu_item.id)
            db.session.add(order_detail)
            db.session.commit()
            flash(f"Added {menu_item.name} to the order for Table {order.table_id}.")
        else:
            flash("Invalid menu item.")
    return redirect(url_for("orders.index"))
