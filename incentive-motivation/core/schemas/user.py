from fastapi_users import schemas

from core.types.user_id import UserIdType


class UserRead(schemas.UserRead[UserIdType]):
    pass


class UserCreate(schemas.UserCreate):
    pass


class UserUpdate(schemas.UserUpdate[UserIdType]):
    pass
