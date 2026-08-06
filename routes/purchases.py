from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Product, Purchase, Supplier

purchases = Blueprint("purchases", __name__)


@purchases.route("/purchases")
@login_required
def purchase_list():

    purchases = Purchase.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "purchases.html",
        purchases=purchases
    )


@purchases.route("/purchases/add", methods=["GET", "POST"])
@login_required
def add_purchase():

    products = Product.query.filter_by(
        user_id=current_user.id
    ).all()

    suppliers = Supplier.query.filter_by(
        user_id=current_user.id
    ).all()

    if request.method == "POST":

        product = Product.query.get(
            request.form.get("product")
        )

        if not product:
            flash("Selected product not found.", "danger")
            return redirect(url_for("purchases.add_purchase"))

        quantity = int(request.form.get("quantity"))

        if quantity <= 0:
            flash("Quantity must be greater than zero.", "danger")
            return redirect(url_for("purchases.add_purchase"))

        purchase_price = float(
            request.form.get("purchase_price")
        )

        if purchase_price <= 0:
            flash("Purchase price must be greater than zero.", "danger")
            return redirect(url_for("purchases.add_purchase"))

        purchase = Purchase(
            user_id=current_user.id,
            product_id=product.id,
            supplier_name=request.form.get("supplier"),
            quantity=quantity,
            purchase_price=purchase_price,
            total_amount=quantity * purchase_price
        )

        # Increase stock
        product.quantity += quantity

        db.session.add(purchase)
        db.session.commit()

        flash("Purchase added successfully!", "success")

        return redirect(url_for("purchases.purchase_list"))

    return render_template(
        "add_purchase.html",
        products=products,
        suppliers=suppliers
    )