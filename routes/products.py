from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user


from models import Product
from extensions import db

products = Blueprint("products", __name__)


# =====================================
# Product List
# =====================================

@products.route("/products")
@login_required
def product_list():

    search = request.args.get("search", "")

    if search:

        products_list = Product.query.filter(
            Product.user_id == current_user.id,
            Product.name.ilike(f"%{search}%")
        ).all()

    else:

        products_list = Product.query.filter_by(
            user_id=current_user.id
        ).all()

    return render_template(
        "products.html",
        products=products_list,
        search=search
    )


# =====================================
# Add Product
# =====================================

@products.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        product = Product(

            user_id=current_user.id,

            name=request.form.get("name"),

            category=request.form.get("category"),

            description=request.form.get("description"),

            purchase_price=float(request.form.get("purchase_price")),

            selling_price=float(request.form.get("selling_price")),

            quantity=int(request.form.get("quantity"))

        )

        db.session.add(product)
        db.session.commit()

        flash("Product added successfully!", "success")

        return redirect(url_for("products.product_list"))

    return render_template("add_product.html")


# =====================================
# Delete Product
# =====================================

@products.route("/products/delete/<int:id>")
@login_required
def delete_product(id):

    product = Product.query.get_or_404(id)

    if product.user_id != current_user.id:

        flash("Unauthorized access.", "danger")

        return redirect(url_for("products.product_list"))

    db.session.delete(product)

    db.session.commit()

    flash("Product deleted successfully.", "success")

    return redirect(url_for("products.product_list"))

# =====================================
# Edit Product
# =====================================

@products.route("/products/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):

    product = Product.query.get_or_404(id)

    if product.user_id != current_user.id:

        flash("Unauthorized access.", "danger")

        return redirect(url_for("products.product_list"))

    if request.method == "POST":

        product.name = request.form.get("name")

        product.category = request.form.get("category")

        product.description = request.form.get("description")

        product.purchase_price = float(
            request.form.get("purchase_price")
        )

        product.selling_price = float(
            request.form.get("selling_price")
        )

        product.quantity = int(
            request.form.get("quantity")
        )

        db.session.commit()

        flash("Product updated successfully!", "success")

        return redirect(url_for("products.product_list"))

    return render_template(
        "edit_product.html",
        product=product
    )