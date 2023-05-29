from flask_sse import sse

class EventStreamer:
    def __init__(self, data, event_type) -> None:
        self.data = data
        self.event_type = event_type
    
    def stream(self):
        sse.publish(
            data = self.data, 
            type = self.event_type)
        
    
    
    