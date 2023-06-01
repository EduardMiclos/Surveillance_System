from .EventStreamer import EventStreamer
from .EventType import EventType

class EventStreamerFactory:
    def __init__(self):
        pass
    
    @staticmethod
    def create(event_type):
        # Define the pre-defined data and event_type mappings
        event_mapping = {
            EventType.HW_DATA_TRANSMISSION_STOP: {"data": "STOP", "type": "DATA_TRANSMISSION"},
            EventType.HW_DATA_TRANSMISSION_START: {"data": "START", "type": "DATA_TRANSMISSION"},
            EventType.HW_DATA_TRANSMISSION_RESTART: {"data": "RESTART", "type": "DATA_TRANSMISSION"},
            EventType.HW_UPDATE: {"data": "<here to be added paths to preprocess files that were updated>", "type": "UPDATE"}
        }
        
        if event_type in event_mapping:
            data = event_mapping[event_type]["data"]
            event_type = event_mapping[event_type]["type"]
            return EventStreamer(data, event_type)
        else:
            raise ValueError(f'ERROR: Invalid event type! The valid event types are {event_mapping}')