from sqlalchemy import CheckConstraint, func
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import *

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('camera_status.id'), nullable=False)
    status = db.relationship('CameraStatus', lazy=True)
    description = db.Column(db.String(500), nullable=True)
    last_restart = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    last_update = db.Column(db.DateTime, nullable=True)
    footages_path = db.Column(db.String(255), unique=True, nullable=False)
    temp_path = db.Column(db.String(255), unique=True, nullable=False)
    
    __table_args__ = (
        CheckConstraint("name != ''", name='non_empty_name_check'),
        CheckConstraint("footages_path != ''", name='non_empty_footages_path_check'),
        CheckConstraint("temp_path != ''", name='non_empty_temp_path_check')
    )
    
    def __repr__(self):
        return '<Camera {}>'.format(self.name)