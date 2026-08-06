
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Customer, Product, Invoice, InvoiceItem

sales = Blueprint("sales", __name__)


@sales.route("/sales")
@login_required
def sale_list():
    invoices = Invoice.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "sales.html",
        invoices=invoices
    )


@sales.route("/sales/new", methods=["GET", "POST"])
@login_required
def new_bill():

    customers = Customer.query.filter_by(
        user_id=current_user.id
    ).all()

    products = Product.query.filter_by(
        user_id=current_user.id
    ).all()

    if request.method == "POST":

        customer_id = int(request.form["customer"])
        product_id = int(request.form["product"])
        quantity = int(request.form["quantity"])

        product = Product.query.get(product_id)

        # Check stock
        if quantity > product.quantity:

            flash("Not enough stock available.", "danger")

            return redirect(
                url_for("sales.new_bill")
            )

        total = quantity * product.selling_price

        invoice = Invoice(
    user_id=current_user.id,
    customer_id=customer_id,
    invoice_number=f"INV-{int(time.time())}",
    total_amount=total,
    discount=0,
    gst_amount=0,
    grand_total=total
)

        db.session.add(invoice)
        db.session.commit()

        item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=product.id,
            quantity=quantity,
            price=product.selling_price,
            total=total
        )

        db.session.add(item)

        # Reduce stock
        product.quantity -= quantity

        db.session.commit()

        flash("Invoice created successfully!", "success")

        return redirect(
            url_for("sales.sale_list")
        )

    return render_template(
        "new_bill.html",
        customers=customers,
        products=products
    )

# =====================================
# View Invoice
# =====================================

@sales.route("/sales/invoice/<int:id>")
@login_required
def view_invoice(id):

    invoice = Invoice.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "invoice.html",
        invoice=invoice
    )