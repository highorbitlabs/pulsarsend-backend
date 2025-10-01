from enum import Enum


class UserRoleEnum(str, Enum):
    customer = 'customer'
    business = 'business'

class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = "other"
