from utils.common_exceptions import AppException


class UserNotFoundException(AppException):
    default_message = 'User not found'


class DuplicateValueException(AppException):
    default_message = 'User with this email already exist'


class RoleNotFoundException(AppException):
    default_message = 'Role not found'
