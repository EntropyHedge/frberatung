from . import create_app
from .extensions import celery

# Configure the application
flask_app = create_app()

# This exposes the celery app for the Celery worker
celery_app = flask_app.extensions["celery"]