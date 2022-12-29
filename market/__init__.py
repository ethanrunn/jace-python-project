from flask import Flask, render_template, request
# from dotenv import dotenv_values
from .database import ENV


def create_app():
    app = Flask(__name__)

    # Configurations
    app.config["SECRET_KEY"] = "my_own"

    # Routes
    from .view.admin import admin

    app.register_blueprint(admin, url_prefix='/admin')
    return app

