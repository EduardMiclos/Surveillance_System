from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from validate_email_address import validate_email
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import *

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    secondname = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def is_email_valid(self):
        return validate_email(self.email)

    __table_args__ = (
        CheckConstraint(is_email_valid == True, name='valid_email_check'),
        CheckConstraint(firstname != '', name='non_empty_firstname_check'),
        CheckConstraint(secondname != '', name='non_empty_secondname_check'),
    )
    
    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    
