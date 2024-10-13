from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Table, Order, MenuItem, MenuItemType, OrderDetails
from app import db

bp = Blueprint("orders", __name__, url_prefix="")

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    tables = Table.query.all()  # Retrieve all table records
    servers = Employee.query.all()  # Retrieve all employees
    orders = Order.query.filter_by(finished=False).all()  # Open orders only

    # Prepare current order and prices
    current_order = orders[0] if orders else None
    order_prices = {}

    for order in orders:
        total_price = sum(item.price for item in MenuItem.query.join(OrderDetails).filter(OrderDetails.order_id == order.id).all())
        order_prices[order.id] = total_price

    # Form handling for table assignment
    if request.method == "POST":
        table_number = request.form.get("table_number")
        server_name = request.form.get("server_name")

        if not table_number or not server_name:
            flash("Table or server not selected.")
        else:
            table = Table.query.filter_by(number=table_number).first()
            server = Employee.query.filter_by(name=server_name).first()

            if not table or not server:
                flash("Invalid table or server.")
            else:
                existing_order = Order.query.filter_by(table_id=table.id, finished=False).first()
                if existing_order:
                    flash(f"Table {table.number} already has an open order.")
                else:
                    new_order = Order(table_id=table.id, employee_id=server.id, finished=False)
                    db.session.add(new_order)
                    db.session.commit()
                    flash(f"Table {table.number} assigned to {server.name}.")
        return redirect(url_for("orders.index"))

    menu_item_types = MenuItemType.query.all()
    return render_template('orders.html', tables=tables, servers=servers, orders=orders, order_prices=order_prices, menu_item_types=menu_item_types, current_order=current_order)



@bp.route("/close_order/<int:order_id>", methods=["POST"])
@login_required
def close_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order.finished = True
        db.session.commit()
        flash(f"Closed order for Table {order.table_id}.")
    return redirect(url_for("orders.index"))


@bp.route("/add_to_order/<int:order_id>", methods=["POST"])
@login_required
def add_to_order(order_id):
    order = Order.query.get(order_id)
    if order:
        # Handling multiple menu items added to the order
        menu_item_ids = request.form.getlist("menu_item_ids")
        if menu_item_ids:
            for item_id in menu_item_ids:
                menu_item = MenuItem.query.get(item_id)
                if menu_item:
                    order_detail = OrderDetails(order_id=order.id, item_id=menu_item.id)
                    db.session.add(order_detail)
            db.session.commit()
            flash("Items added to the order.")
        else:
            flash("No items selected.")
    return redirect(url_for("orders.index"))
