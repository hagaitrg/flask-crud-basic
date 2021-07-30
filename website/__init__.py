from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "hellomfs"

    # Mengambil semua fungsi dari class views dan auth
    from .views import views
    from .auth import auth

    # sebelum route dari kelas tersebut di akses harusdi awali dengan url prefix pada blueprint
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app