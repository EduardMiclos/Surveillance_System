from flask_sse import sse

class EventStreamer:
    def __init__(self) -> None:
        self.data = {}
        self.type = None  
    
    def stream(self):
        sse.publish(
            data = self.data, 
            type = self.type)
        
    
    
    