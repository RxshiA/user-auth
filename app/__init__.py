from flask import Flask
from flask_migrate import Migrate

from app.models import db
from config import config_by_name

migrate = Migrate()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import register_blueprints
    register_blueprints(app)

    return app
