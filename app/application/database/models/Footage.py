from flask_login import UserMixin
from sqlalchemy import CheckConstraint, func
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import *

class Footage(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False, default=func.current_date())
    path = db.Column(db.String(255), unique=True, nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    camera = db.relationship('Camera', backref='footage', lazy=True)
    
    __table_args__ = (
        CheckConstraint("name != ''", name='non_empty_name_check'),
        CheckConstraint("path != ''", name='non_empty_path_check'),
        CheckConstraint("date != ''", name='non_empty_date_check'),
    )
    
    def __repr__(self):
        return '<Footage {}>'.format(self.name)