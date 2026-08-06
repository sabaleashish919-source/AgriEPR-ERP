from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# -------------------------------------------------
# Login Manager
# -------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =================================================
# USER MODEL
# =================================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    mobile = db.Column(db.String(15))

    shop_name = db.Column(db.String(100))

    shop_address = db.Column(db.Text)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="admin")

    profile_image = db.Column(
        db.String(200),
        default="default.png"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationships

    products = db.relationship(
        "Product",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    customers = db.relationship(
        "Customer",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )
    suppliers = db.relationship(
    "Supplier",
    backref="owner",
    lazy=True,
    cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"


# =================================================
# PRODUCT MODEL
# =================================================

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(db.String(150), nullable=False)

    category = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    purchase_price = db.Column(db.Float, nullable=False)

    selling_price = db.Column(db.Float, nullable=False)

    quantity = db.Column(db.Integer, default=0)

    image = db.Column(
        db.String(200),
        default="default_product.png"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Product {self.name}>"


# =================================================
# CUSTOMER MODEL
# =================================================

class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    customer_name = db.Column(
        db.String(100),
        nullable=False
    )

    mobile = db.Column(
        db.String(15),
        nullable=False
    )

    email = db.Column(
        db.String(120)
    )

    address = db.Column(
        db.Text
    )

    gst_number = db.Column(
        db.String(30)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Customer {self.customer_name}>"
    
# =================================================
# SUPPLIER MODEL
# =================================================

class Supplier(db.Model):

    __tablename__ = "suppliers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    supplier_name = db.Column(
        db.String(150),
        nullable=False
    )

    mobile = db.Column(
        db.String(15)
    )

    email = db.Column(
        db.String(120)
    )

    address = db.Column(
        db.Text
    )

    gst_number = db.Column(
        db.String(30)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

   

    def __repr__(self):
        return f"<Supplier {self.supplier_name}>"
    
# =================================================
# PURCHASE MODEL
# =================================================

class Purchase(db.Model):

    __tablename__ = "purchases"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    supplier_name = db.Column(
        db.String(150),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    purchase_price = db.Column(
        db.Float,
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    purchase_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationships

    product = db.relationship(
        "Product",
        backref="purchase_history"
    )

    user = db.relationship(
        "User",
        backref="purchases"
    )

    def __repr__(self):
        return f"<Purchase {self.id}>"
    

# =================================================
# INVOICE MODEL
# =================================================

class Invoice(db.Model):

    __tablename__ = "invoices"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    # Professional Invoice Number
    invoice_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    # Billing Information
    total_amount = db.Column(
        db.Float,
        default=0
    )

    discount = db.Column(
        db.Float,
        default=0
    )

    gst_amount = db.Column(
        db.Float,
        default=0
    )

    grand_total = db.Column(
        db.Float,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    customer = db.relationship(
        "Customer",
        backref="invoices"
    )

    user = db.relationship(
        "User",
        backref="invoices"
    )

    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"


# =================================================
# INVOICE ITEM MODEL
# =================================================

class InvoiceItem(db.Model):

    __tablename__ = "invoice_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey("invoices.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    total = db.Column(
        db.Float,
        nullable=False
    )

    invoice = db.relationship(
        "Invoice",
        backref="items"
    )

    product = db.relationship(
        "Product"
    )