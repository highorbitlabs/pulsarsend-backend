from starlette import status


class AppException(Exception):
    default_message = "Something went wrong"
    default_code = status.HTTP_400_BAD_REQUEST
    default_dev_message = ""

    def __init__(self, message=None, code=None, dev_message=None):
        self.message = message if message else self.default_message
        self.code = code if code else self.default_code
        self.dev_message = dev_message if dev_message else self.default_dev_message


class NotFoundException(AppException):
    default_message = "Object not found"
    default_code = status.HTTP_404_NOT_FOUND


class PermissionDeniedException(AppException):
    default_message = "Permission denied"
    default_code = status.HTTP_403_FORBIDDEN


class InvalidQueryParamsException(AppException):
    default_message = "Invalid query params"
    default_code = status.HTTP_400_BAD_REQUEST


class NotImplementedException(AppException):
    default_message = "Subclasses should implement this"
    default_code = status.HTTP_501_NOT_IMPLEMENTED


class ExternalServiceException(AppException):
    default_message = "External service error"
    default_code = status.HTTP_502_BAD_GATEWAY


class PrivyApiException(ExternalServiceException):
    default_message = "Privy API request failed"
