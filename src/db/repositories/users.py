from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from api.schemas.auth import UserCredentialsSchema, UserSchema
from db.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.__hash_manager = PasswordHasher()

    def verify_password(self, password_hash: str, password: str) -> bool:
        # Returns True if passwords are the same, False otherwise.
        try:
            self.__hash_manager.verify(password_hash, password)
            return True
        except VerifyMismatchError:
            return False

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            text("SELECT * FROM users WHERE id = :id"),
            {"id": user_id}
        )
        row = result.fetchone()
        return row._mapping if row else None

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username}
        )
        row = result.fetchone()
        return row._mapping if row else None

    async def create_user(self, user_creds: UserCredentialsSchema) -> int | None:
        try:
            result = await self.session.execute(
                text("INSERT INTO users (username, password) VALUES (:username, :password) RETURNING *"),
                {"username": user_creds.username, "password": self.__hash_manager.hash(user_creds.password)}
            )
            await self.session.commit()
            row = result.fetchone()
            return row.id
        except IntegrityError:
            await self.session.rollback()
            return None
