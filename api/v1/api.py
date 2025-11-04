from fastapi import APIRouter

from api.v1.auth.auth_endpoints import router as auth_router
from api.v1.users.user_endpoints import router as user_router
from api.v1.notifications.notification_endpoints import router as notification_router


# Mount feature routers here as the API surface expands.
v1_router = APIRouter()
v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(notification_router)
