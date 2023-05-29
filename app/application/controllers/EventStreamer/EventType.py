from enum import Enum

class EventType(Enum):
    HW_DATA_TRANSMISSION_STOP = 1,
    HW_DATA_TRANSMISSION_START = 2,
    HW_DATA_TRANSMISSION_RESTART = 3,
    HW_UPDATE = 4