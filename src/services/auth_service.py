from typing import Annotated, TypeAlias, TypedDict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models import User
from db.repositories.users import UserRepo
from api.schemas.auth import UserCredentialsSchema

JWT: TypeAlias = Annotated[str, "JWT"]


class JWTPayload(TypedDict):
    user_id: str
    exp: int


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.repo = UserRepo(session)

    @staticmethod
    def __create_jwt(user_id: int) -> JWT:
        ...

    @staticmethod
    def __decode_jwt(access_token: JWT) -> JWTPayload | None:
        ...

    async def register(self, user_creds: UserCredentialsSchema) -> JWT | None:
        ...

    async def login(self, user_creds: UserCredentialsSchema) -> JWT | None:
        ...

    async def get_user(self, access_token: JWT) -> User | None:
        ...
