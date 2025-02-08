from fastapi import APIRouter

from api.dependencies.authentication.backend import authentication_backend
from api.api_v1.fastapi_users import fastapi_users
from core.config import settings


router = APIRouter(
    prefix=settings.api.v1.prefix,
    tags=["Auth"],
)

router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend),
)
