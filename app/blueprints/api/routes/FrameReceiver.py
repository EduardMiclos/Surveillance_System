from flask_restful import Resource

class FrameReceiver(Resource):
    def get(self):
        return "A JSON file"