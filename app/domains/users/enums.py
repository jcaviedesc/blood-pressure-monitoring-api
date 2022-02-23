from enum import Enum, IntEnum

class GenderEnum(str, Enum):
    male = "M"
    female = "F"


class SIsystemUnitEnum(str, Enum):
    second = "s"
    metre = "m"
    kilogram = "Kg"


class UserTypeEnum(IntEnum):
    health_professional = 1
    normal = 2


class HealthInfoEnum(str, Enum):
    yes = "Y"
    no = "N"
    not_know = "NK"