from flask import Flask
from .extensions import login_manager, db
import logging
from logging.handlers import RotatingFileHandler


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # replace in production or via .env
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Logging setup
    handler = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Initialize extensions
    login_manager.init_app(app)
    db.init_app(app)

    # Register blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.recipes import recipes_bp
    from .blueprints.logs import logs_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(logs_bp)

    @app.route('/')
    def root():
        from flask_login import current_user
        from flask import redirect, url_for
        if current_user.is_authenticated:
            return redirect(url_for('recipes.list_recipes'))
        return redirect(url_for('auth.login'))

    @app.errorhandler(403)
    def forbidden(e):
        return ("Forbidden", 403)

    @app.errorhandler(404)
    def not_found(e):
        return ("Not Found", 404)

    return app
