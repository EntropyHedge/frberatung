import os
import logging
from logging.handlers import RotatingFileHandler
import json
from flask import Flask, render_template, session
from flask_session import Session
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_talisman import Talisman
from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, cache, limiter, talisman, login_manager, configure_celery
from .blueprints.main import main_bp
from .blueprints.auth import auth_bp
from .blueprints.api import api_bp


def create_app(config_class=None):
    # pick config via FLASK_ENV unless caller supplies one
    if config_class is None:
        env = os.getenv("FLASK_ENV", "development")
        config_class = ProductionConfig if env == "production" else DevelopmentConfig

    app = Flask(__name__)
    #Define the prefix for the app
    app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(config_class)
    
    # --- initialise extensions -------------------------------------------------
    db.init_app(app)
    migrate = Migrate(app, db)
    Session(app)
    cache.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)
    
    # Configure Flask-Login user loader and anonymous user
    from . import auth_utils

    # --- Flask-Talisman --------------------------------------------------------
    Talisman(
        app,
        force_https=app.config["TALISMAN_FORCE_HTTPS"],
        content_security_policy=app.config["TALISMAN_CSP"],
    )
    
    # Set up logging (only if not in debug mode)
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')

   
    #Register blueprints and other components here
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    configure_celery(app)

    # Register CLI commands
    from . import commands
    commands.register_commands(app)

    return app