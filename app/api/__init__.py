from .auth_routes import auth_blueprint
from .user_routes import user_blueprint


def register_blueprints(app):
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')

    # Health check at root
    @app.route('/')
    def health():
        return {'status': 'OK'}, 200
