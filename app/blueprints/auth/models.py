from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin):
    """User class for Flask-Login session-based authentication"""
    
    def __init__(self, id: str, email: str = None, name: str = None, paid: bool = False):
        self.id = id
        self.email = email
        self.name = name
        self.paid = paid
    
    def get_id(self) -> str:
        return str(self.id)
    
    @property
    def is_authenticated(self) -> bool:
        return True
    
    @property
    def is_active(self) -> bool:
        return True
    
    @property
    def is_anonymous(self) -> bool:
        return False


class AnonymousUser(AnonymousUserMixin):
    """Anonymous user with safe defaults to prevent AttributeError"""
    
    id = None
    email = None
    name = "Guest"
    paid = False
    
    @property
    def is_authenticated(self) -> bool:
        return False
    
    @property
    def is_active(self) -> bool:
        return False
    
    @property
    def is_anonymous(self) -> bool:
        return True
