from starlette.requests import Request
from starlette.responses import JSONResponse

from utils.common_exceptions import AppException


async def app_error_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        {
            "status_code": exc.code,
            "error_message": exc.message,
            "code": "",
            "developer_message": exc.dev_message,
        },
        status_code=exc.code,
    )
