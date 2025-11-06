from utils.common_exceptions import AppException


class UserNotFoundException(AppException):
    default_message = 'User not found'


class DuplicateValueException(AppException):
    default_message = 'User with this email already exist'


class RoleNotFoundException(AppException):
    default_message = 'Role not found'


class UserVaultNotFoundException(AppException):
    default_message = 'User vault not found'


class UserVaultAlreadyExistsException(AppException):
    default_message = 'User vault already exists'
