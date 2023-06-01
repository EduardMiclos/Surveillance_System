from .EventStreamer import EventStreamer
from .EventType import EventType

class EventStreamerFactory:
    event_mapping = {
            EventType.HW_DATA_TRANSMISSION_ALTER: {"data": "", "type": 'HW_DATA_TRANSMISSION_ALTER'},
            EventType.HW_UPDATE: {"data": "<here to be added paths to preprocess files that were updated>", "type": 'HW_UPDATE'},
            EventType.MANAGE_USER_REFRESH: {"data": "", "type": 'USER_REFRESH'},
            EventType.MANAGE_FOOTAGES_REFRESH: {"data": "", "type": 'FOOTAGES_REFRESH'},
            EventType.MANAGE_CAMERA_REFRESH: {"data": "", "type": 'CAMERA_REFRESH'}
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
            raise ValueError(f'ERROR: Invalid event type! The valid event types are {EventStreamerFactory.event_mapping}')