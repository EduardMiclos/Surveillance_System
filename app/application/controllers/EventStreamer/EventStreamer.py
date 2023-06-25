from flask_sse import sse
import json

class EventStreamer:
    def __init__(self, event_type) -> None:
        self.data = {}
        self.event_type = event_type
    
    def stream(self):
        sse.publish(
            {
                "message": self.event_type,
                "data": json.dumps(self.data)
            },
            type = self.event_type)
        
    def add_data(self, key, value):
        self.data[key] = value