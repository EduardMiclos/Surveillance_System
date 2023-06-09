from enum import Enum

class EventType(Enum):
    HW_DATA_TRANSMISSION_ALTER = 1,
    RASP_UPDATE = 2,
    RASP_EDIT = 3,
    RASP_REMOVE = 4,
    RASP_START = 5,
    RASP_STOP = 6,
    MANAGE_USER_REFRESH = 7,
    MANAGE_FOOTAGES_REFRESH = 8,
    MANAGE_CAMERA_REFRESH = 9