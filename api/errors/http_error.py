from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        {
            "status_code": exc.status_code,
            "error_message": exc.detail,
            "code": "",
            "developer_message": "",
        },
        status_code=exc.status_code,
    )
