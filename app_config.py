import os
from werkzeug.security import generate_password_hash

SECRET_KEY = os.environ.get('SECRET_KEY', generate_password_hash('verySpecialKeyToKeep'))
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "lib-system.db")
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = os.environ.get('EMAIL', 'hridayahoney@gmail.com')
MAIL_PASSWORD = os.environ.get('PASSWORD')
MAIL_USE_TLS = True
JSON_SORT_KEYS = False
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
