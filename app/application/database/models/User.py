from flask_login import UserMixin
from sqlalchemy import CheckConstraint, func
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import *

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    secondname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __table_args__ = (
        CheckConstraint(firstname != '', name='non_empty_firstname_check'),
        CheckConstraint(secondname != '', name='non_empty_secondname_check'),
        CheckConstraint("register_date != ''", name='non_empty_register_date_check'),
    )
    
    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    

