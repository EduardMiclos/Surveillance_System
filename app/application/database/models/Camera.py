import os

from sqlalchemy import CheckConstraint, func
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import *
from .config import FOOTAGE_PATH

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('camera_status.id'), nullable=False, default=1)
    status = db.relationship('CameraStatus', lazy=True)
    description = db.Column(db.String(500), nullable=True)
    last_restart = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    last_update = db.Column(db.DateTime, nullable=True)
    footages_path = db.Column(db.String(255), unique=True, nullable=False)
    temp_path = db.Column(db.String(255), unique=True, nullable=False)
    preprocess_data = db.Column(db.Boolean(), nullable=True, default=False)
    current_detections = db.Column(db.Integer, default = 0)
    
    __table_args__ = (
        CheckConstraint("name != ''", name='non_empty_name_check'),
        CheckConstraint("footages_path != ''", name='non_empty_footages_path_check'),
        CheckConstraint("temp_path != ''", name='non_empty_temp_path_check')
    )
    
    def __init__(self, name, status_id=1, description=None, footages_path=None, temp_path=None, preprocess_data=None, current_detections=0):
        self.name = name
        self.status_id = status_id
        self.description = description
        self.preprocess_data = preprocess_data
        self.current_detections = current_detections
        
        if footages_path is not None:
            self.footages_path = footages_path
        else:
            self.footages_path = self.name  # Set default value as the Camera name

        if temp_path is not None:
            self.temp_path = temp_path
        else:
            self.temp_path = self.name  # Set default value as the Camera name
            
        os.mkdir(f'{FOOTAGE_PATH}/{self.footages_path}')
        os.mkdir(f'{FOOTAGE_PATH}/temp/{self.temp_path}')
        
        
    
    def __repr__(self):
        return '<Camera {}>'.format(self.name)