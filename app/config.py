import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret_jwt')
