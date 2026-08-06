from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import Product, Customer, Supplier, Purchase, Invoice

reports = Blueprint("reports", __name__)


@reports.route("/reports")
@login_required
def report_list():

    total_products = Product.query.filter_by(user_id=current_user.id).count()

    total_customers = Customer.query.filter_by(user_id=current_user.id).count()

    total_suppliers = Supplier.query.filter_by(user_id=current_user.id).count()

    total_purchases = Purchase.query.filter_by(user_id=current_user.id).count()

    total_sales = Invoice.query.filter_by(user_id=current_user.id).count()

    total_revenue = sum(
        invoice.grand_total
        for invoice in Invoice.query.filter_by(
            user_id=current_user.id
        ).all()
    )

    return render_template(
        "reports.html",
        total_products=total_products,
        total_customers=total_customers,
        total_suppliers=total_suppliers,
        total_purchases=total_purchases,
        total_sales=total_sales,
        total_revenue=total_revenue
    )