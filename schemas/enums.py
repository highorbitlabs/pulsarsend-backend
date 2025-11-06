from enum import Enum


class UserRoleEnum(str, Enum):
    customer = 'customer'
    business = 'business'

class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = "other"

class NotificationPriorityEnum(str, Enum):
    high = 'high'
    normal = 'normal'


class NotificationPriorityEnum(str, Enum):
    high = 'high'
    normal = 'normal'


class NotificationStatusEnum(str, Enum):
    queued = "queued"
    sent = "sent"
    failed = "failed"


class NotificationPlatformEnum(str, Enum):
    android = "android"
    ios = "ios"
    web = "web"


class TransactionEnum(str, Enum):
    deposit = "deposit"
    withdraw = "withdraw"

