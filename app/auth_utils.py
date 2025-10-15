from flask import session
from .extensions import login_manager
from .blueprints.auth.models import User, AnonymousUser


# Configure anonymous user for Flask-Login
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """Load user from session data"""
    user_data = session.get('user_info')
    if not user_data:
        return None
    return User(
        id=user_id,
        email=user_data.get('email'),
        name=user_data.get('name'),
        paid=user_data.get('paid', False)
    )