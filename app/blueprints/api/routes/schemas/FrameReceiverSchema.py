from flask_marshmallow import Schema
from marshmallow import fields, validate, ValidationError

class FrameReceiverSchema(Schema):        
    frames = fields.List(fields.Float(), required = True)
    chunk_size = fields.Integer(required = True)
    frame_width = fields.Integer(required = True)
    frame_height = fields.Integer(required = True)
        
frame_receiver_schema = FrameReceiverSchema()