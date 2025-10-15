from functools import wraps
from flask import request, jsonify, g
from flask_login import current_user
from .models import ApiKey
from datetime import datetime
from app.extensions import db

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is already authenticated via Flask-Login, allow access
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        
        # Otherwise, check for API key in headers or query parameters
        api_key = request.headers.get('X-API-Key')
        
        # Only look in query parameters if not in headers
        if not api_key and 'api_key' in request.args:
            api_key = request.args.get('api_key')
            # Create a modified args multidictionary that doesn't include api_key
            args_copy = request.args.copy()
            args_copy.pop('api_key')
            # Replace request.args with our filtered version
            request.args = args_copy
        
        if not api_key:
            return jsonify({'error': 'Authentication required'}), 401
            
        # Validate API key
        key_record = ApiKey.query.filter_by(key=api_key).first()
        if not key_record:
            return jsonify({'error': 'Invalid API key'}), 401
            
        # Update last used timestamp
        key_record.last_used_at = datetime.utcnow()
        db.session.commit()
        
        # Store user_id from API key for access in the view function
        g.user_id = key_record.user_id
        
        return f(*args, **kwargs)
    return decorated_function
