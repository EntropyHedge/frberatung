from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_login import LoginManager
from celery import Celery, Task
from flask import Flask
import os

talisman = Talisman()
login_manager = LoginManager()
cache = Cache()
db = SQLAlchemy()

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{REDIS_HOST}:6379/1"
)

celery = Celery()  # Create a standalone celery instance

def configure_celery(app):
    """Configure Celery with Flask app settings"""
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.conf.update(app.config["CELERY"])
    celery.Task = FlaskTask
    app.extensions["celery"] = celery
    return celery

def get_celery_app():
    """Return the configured Celery app from current Flask app."""
    from flask import current_app
    return current_app.extensions["celery"]


