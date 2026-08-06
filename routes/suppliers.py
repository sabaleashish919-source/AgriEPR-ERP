from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Supplier

suppliers = Blueprint("suppliers", __name__)


# ===============================
# Supplier List
# ===============================

@suppliers.route("/suppliers")
@login_required
def supplier_list():

    suppliers = Supplier.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "suppliers.html",
        suppliers=suppliers
    )


# ===============================
# Add Supplier
# ===============================

@suppliers.route("/suppliers/add", methods=["GET", "POST"])
@login_required
def add_supplier():

    if request.method == "POST":

        supplier = Supplier(
            user_id=current_user.id,
            supplier_name=request.form.get("supplier_name"),
            mobile=request.form.get("mobile"),
            email=request.form.get("email"),
            address=request.form.get("address"),
            gst_number=request.form.get("gst_number")
        )

        db.session.add(supplier)
        db.session.commit()

        flash("Supplier added successfully!", "success")

        return redirect(url_for("suppliers.supplier_list"))

    return render_template("add_supplier.html")


# ===============================
# Edit Supplier
# ===============================

@suppliers.route("/suppliers/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_supplier(id):

    supplier = Supplier.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        supplier.supplier_name = request.form.get("supplier_name")
        supplier.mobile = request.form.get("mobile")
        supplier.email = request.form.get("email")
        supplier.address = request.form.get("address")
        supplier.gst_number = request.form.get("gst_number")

        db.session.commit()

        flash("Supplier updated successfully!", "success")

        return redirect(url_for("suppliers.supplier_list"))

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )


# ===============================
# Delete Supplier
# ===============================

@suppliers.route("/suppliers/delete/<int:id>")
@login_required
def delete_supplier(id):

    supplier = Supplier.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(supplier)
    db.session.commit()

    flash("Supplier deleted successfully!", "success")

    return redirect(url_for("suppliers.supplier_list"))