from flask_marshmallow import Schema
from marshmallow import fields, validate

class FrameReceiverSchema(Schema):        
    frames = fields.List(fields.Float(), required = True)
    chunk_size = fields.Integer(required = True, validate = validate.Equal(32))
    channels = fields.Integer(required = True, validate = validate.Equal(3))
    frame_width = fields.Integer(required = True, validate = validate.Range(min = 100, max = 800))
    frame_height = fields.Integer(required = True, validate = validate.Range(min = 100, max = 800))
        
frame_receiver_schema = FrameReceiverSchema()