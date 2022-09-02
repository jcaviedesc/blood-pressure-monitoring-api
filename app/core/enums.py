from enum import Enum, IntEnum

class PageLimitEnum(IntEnum):
    small = 9
    medium = 18
    large = 27

class usersTypesEnum(str, Enum):
    PATIENT = "patient"
    PROFESSIONAL = "professional"

class GenderEnum(str, Enum):
    male = "M"
    female = "F"


class SIsystemUnitEnum(str, Enum):
    second = "s"
    metre = "m"
    kilogram = "Kg"

class AsystemUnitEnum(str, Enum):
    centimeter = 'cm'


class UserTypeEnum(IntEnum):
    health_professional = 1
    patient = 2


class HealthInfoEnum(str, Enum):
    yes = "Y"
    no = "N"
    not_know = "NK"

class FindUserActions(str,Enum):
    is_new = 'isNew'

class CardiovascularRiskOption(str, Enum):
    HIGHT = 'hight'
    MEDIUM = 'medium'
    LOW = 'LOW'