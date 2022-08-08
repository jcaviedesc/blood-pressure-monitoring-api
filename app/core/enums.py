from enum import Enum, IntEnum

class PageLimitEnum(IntEnum):
    small = 9
    medium = 18
    large = 27

class usersTypesEnum(Enum, str):
    PATIENT = "patient"
    PROFESSIONAL = "professional"
