from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import (
    Product,
    Customer,
    Supplier,
    Purchase,
    Invoice
)

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def home():

    total_products = Product.query.filter_by(
        user_id=current_user.id
    ).count()

    total_customers = Customer.query.filter_by(
        user_id=current_user.id
    ).count()

    total_suppliers = Supplier.query.filter_by(
        user_id=current_user.id
    ).count()

    total_purchases = Purchase.query.filter_by(
        user_id=current_user.id
    ).count()

    total_sales = Invoice.query.filter_by(
        user_id=current_user.id
    ).count()

    total_revenue = sum(
        invoice.grand_total
        for invoice in Invoice.query.filter_by(
            user_id=current_user.id
        ).all()
    )

    total_purchase_cost = sum(
        purchase.total_amount
        for purchase in Purchase.query.filter_by(
            user_id=current_user.id
        ).all()
    )

    profit = total_revenue - total_purchase_cost

    low_stock = Product.query.filter(
        Product.user_id == current_user.id,
        Product.quantity < 10
    ).count()

    return render_template(
        "dashboard.html",
        user=current_user,
        total_products=total_products,
        total_customers=total_customers,
        total_suppliers=total_suppliers,
        total_purchases=total_purchases,
        total_sales=total_sales,
        total_revenue=total_revenue,
        profit=profit,
        low_stock=low_stock
    )