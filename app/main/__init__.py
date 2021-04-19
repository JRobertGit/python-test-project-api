from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cache = Cache()

from .config import config
from .views.users import users_view
from .controllers.users import users_api


def create_app(config_name):
    app = Flask(__name__)
    # Configuration
    app.config.from_object(config[config_name])
    # Database
    db.init_app(app)
    # Routes (Views & API)
    app.register_blueprint(users_view)
    app.register_blueprint(users_api)
    # Caching
    cache.init_app(app)

    return app
