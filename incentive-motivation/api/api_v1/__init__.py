from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer

from core.config import settings

from .auth import router as auth_router
from .users import router as users_router
from .incentive_list import router as incentive_list_router
from .incentive import router as incentive_router
from .lottery import router as lottery_router
from .purpose import router as purpose_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(incentive_list_router)
router.include_router(incentive_router)
router.include_router(lottery_router)
router.include_router(purpose_router)
