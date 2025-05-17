from flask import Flask
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.models import db
from config import config_by_name

migrate = Migrate()
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    from app.api import register_blueprints
    register_blueprints(app)

    return app
