from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from models import User
from extensions import db

auth = Blueprint("auth", __name__)


# -----------------------------
# LOGIN
# -----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            flash("Welcome back!", "success")

            return redirect(url_for("dashboard.home"))

        flash("Invalid Email or Password!", "danger")

        return redirect(url_for("auth.login"))

    return render_template("login.html")


# -----------------------------
# REGISTER
# -----------------------------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        shop_name = request.form.get("shop_name")
        shop_address = request.form.get("shop_address")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            mobile=mobile,
            shop_name=shop_name,
            shop_address=shop_address,
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful! Please Login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -----------------------------
# LOGOUT
# -----------------------------
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))