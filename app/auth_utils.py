from flask import session
from .extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    user_data = session.get('user_info')
    if not user_data:
        return None
    return User(
        id=user_id,
        email=user_data.get('email'),
        name=user_data.get('name'),
        paid=user_data.get('paid', False)
    )