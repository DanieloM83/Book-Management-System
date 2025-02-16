from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.auth import UserCredentialsSchema
from db.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: str) -> User | None:
        ...

    async def get_user_by_username(self, username: str) -> User | None:
        ...

    async def create_user(self, user_creds: UserCredentialsSchema) -> int:
        ...
