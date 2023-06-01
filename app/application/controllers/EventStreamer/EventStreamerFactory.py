from .EventStreamer import EventStreamer
from .EventType import EventType

class EventStreamerFactory:
    event_mapping = {
            EventType.HW_DATA_TRANSMISSION_STOP: {"data": "STOP", "type": "DATA_TRANSMISSION"},
            EventType.HW_DATA_TRANSMISSION_START: {"data": "START", "type": "DATA_TRANSMISSION"},
            EventType.HW_DATA_TRANSMISSION_RESTART: {"data": "RESTART", "type": "DATA_TRANSMISSION"},
            EventType.HW_UPDATE: {"data": "<here to be added paths to preprocess files that were updated>", "type": "UPDATE"}
        }
    
    def __init__(self):
        pass
        
    @staticmethod
    def create(event_type):
        if event_type in EventStreamerFactory.event_mapping:
            data = EventStreamerFactory.event_mapping[event_type]["data"]
            event_type = EventStreamerFactory.event_mapping[event_type]["type"]
            return EventStreamer(data, event_type)
        else:
            raise ValueError(f'ERROR: Invalid event type! The valid event types are {event_mapping}')