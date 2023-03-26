from flask import Flask
from flask_restful import Api, Resource


class FrameReceiver(Resource):
    route = '/sendframes'

    def get(self):
        return "A JSON file"