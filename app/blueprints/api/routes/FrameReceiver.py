from flask_restful import Resource, request

if __name__ == "__main__":
    from schemas.FrameReceiverSchema import frame_receiver_schema
else:
    from .schemas.FrameReceiverSchema import frame_receiver_schema

class FrameReceiver(Resource):
    def post(self):
        form_data = request.get_json();
        
        errors = frame_receiver_schema.validate(form_data)
        return "123"