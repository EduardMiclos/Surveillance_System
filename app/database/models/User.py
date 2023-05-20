from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from validate_email_address import validate_email

from ..database import *

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    secondname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False)

    @hybrid_property
    def is_email_valid(self):
        return validate_email(self.email)

    __table_args__ = (
        CheckConstraint(is_email_valid == True, name='valid_email_check'),
        CheckConstraint(firstname != '', name='non_empty_firstname_check'),
        CheckConstraint(secondname != '', name='non_empty_secondname_check'),
    )
    
    
