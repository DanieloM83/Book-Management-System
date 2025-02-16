from time import time
from typing import Annotated, TypeAlias, TypedDict, get_type_hints

import jwt
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
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
        payload = JWTPayload(
            user_id=str(user_id),
            exp=int(time()) + settings.COOKIE_AGE,
        )
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    @staticmethod
    def __decode_jwt(access_token: JWT) -> JWTPayload | None:
        # Returns None if JWT is expired.
        try:
            payload: JWTPayload = jwt.decode(
                access_token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
                options={"require": list(get_type_hints(JWTPayload).keys())},
            )
        except jwt.ExpiredSignatureError:
            return None
        return payload

    async def register(self, user_creds: UserCredentialsSchema) -> JWT | None:
        # Create new user, returns JWT if successful, None if username is already taken.
        user_id = await self.repo.create_user(user_creds)
        if user_id is None:
            return None
        return self.__create_jwt(user_id)

    async def login(self, user_creds: UserCredentialsSchema) -> JWT | None:
        # Returns JWT if successful, None otherwise.
        user = await self.repo.get_user_by_username(user_creds.username)
        if user is None or not self.repo.verify_password(
                user.password, user_creds.password
        ):
            return None
        return self.__create_jwt(user.id)

    async def get_user(self, access_token: JWT) -> User | None:
        # Returns user if JWT is valid, None otherwise.
        payload = self.__decode_jwt(access_token)
        if payload is None:
            return None
        print(payload)
        user = await self.repo.get_user_by_id(int(payload["user_id"]))
        if user is None:
            return None
        return user
