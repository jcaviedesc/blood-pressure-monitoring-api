from enum import Enum, IntEnum

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