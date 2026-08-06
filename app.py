from flask import Flask, render_template

from config import Config
from extensions import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message = "Please login first."


from models import User , Product

with app.app_context():
    db.create_all()


# -------------------
# Blueprints
# -------------------

from routes.auth import auth
from routes.dashboard import dashboard
from routes.products import products
from routes.customers import customers
from routes.suppliers import suppliers
from routes.sales import sales
from routes.reports import reports
from routes.purchases import purchases

app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(products)
app.register_blueprint(customers)
app.register_blueprint(suppliers)
app.register_blueprint(sales)
app.register_blueprint(reports)
app.register_blueprint(purchases)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)