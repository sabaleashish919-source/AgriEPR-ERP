from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Customer

customers = Blueprint("customers", __name__)


# ==========================
# Customer List
# ==========================

@customers.route("/customers")
@login_required
def customer_list():

    customers_list = Customer.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "customers.html",
        customers=customers_list,
        user=current_user
    )


# ==========================
# Add Customer
# ==========================

@customers.route("/customers/add", methods=["GET", "POST"])
@login_required
def add_customer():

    if request.method == "POST":

        customer = Customer(
            user_id=current_user.id,
            customer_name=request.form.get("customer_name"),
            mobile=request.form.get("mobile"),
            email=request.form.get("email"),
            address=request.form.get("address"),
            gst_number=request.form.get("gst_number")
        )

        db.session.add(customer)
        db.session.commit()

        flash("Customer added successfully!", "success")

        return redirect(url_for("customers.customer_list"))

    return render_template(
        "add_customer.html",
        user=current_user
    )


# ==========================
# Edit Customer
# ==========================

@customers.route("/customers/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_customer(id):

    customer = Customer.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        customer.customer_name = request.form.get("customer_name")
        customer.mobile = request.form.get("mobile")
        customer.email = request.form.get("email")
        customer.address = request.form.get("address")
        customer.gst_number = request.form.get("gst_number")

        db.session.commit()

        flash("Customer updated successfully!", "success")

        return redirect(url_for("customers.customer_list"))

    return render_template(
        "edit_customer.html",
        customer=customer
    )


# ==========================
# Delete Customer
# ==========================

@customers.route("/customers/delete/<int:id>")
@login_required
def delete_customer(id):

    customer = Customer.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(customer)
    db.session.commit()

    flash("Customer deleted successfully!", "success")

    return redirect(url_for("customers.customer_list"))