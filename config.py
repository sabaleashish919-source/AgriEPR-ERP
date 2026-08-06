import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for sessions
    SECRET_KEY = "shopmanagement_secret_key_2026"

    # SQLite Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "shop.db")

    # Disable modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload Folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    # Maximum Upload Size (20 MB)
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    # Allowed Image Extensions
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}