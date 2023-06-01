from .EventStreamer import EventStreamer
from .EventType import EventType

class EventStreamerFactory:
    event_mapping = {
            EventType.HW_DATA_TRANSMISSION_ALTER: {"type": 'HW_DATA_TRANSMISSION_ALTER'},
            EventType.RASP_UPDATE: {"type": 'RASP_UPDATE'},
            EventType.RASP_REMOVE: {"type": 'RASP_REMOVE'},
            EventType.MANAGE_USER_REFRESH: {"type": 'USER_REFRESH'},
            EventType.MANAGE_FOOTAGES_REFRESH: {"type": 'FOOTAGES_REFRESH'},
            EventType.MANAGE_CAMERA_REFRESH: {"type": 'CAMERA_REFRESH'}
        }
    
    def __init__(self):
        pass
        
    @staticmethod
    def create(event_type):
        if event_type in EventStreamerFactory.event_mapping:
            event_type = EventStreamerFactory.event_mapping[event_type]["type"]
            return EventStreamer(event_type)
        else:
            raise ValueError(f'ERROR: Invalid event type! The valid event types are {EventStreamerFactory.event_mapping}')