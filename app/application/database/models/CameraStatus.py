from flask_login import UserMixin
from sqlalchemy import CheckConstraint, func
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import *

class CameraStatus(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    
    __table_args__ = (
        CheckConstraint("name != ''", name='non_empty_name_check'),
    )
    
    def __repr__(self):
        return '<CameraStatus {}>'.format(self.name)