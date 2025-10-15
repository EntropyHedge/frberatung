from app.extensions import db
from datetime import datetime
import secrets

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.String(36), nullable=False, index=True)  
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)
    
    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(32)
