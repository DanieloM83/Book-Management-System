from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.config import settings

engine = create_async_engine(url=settings.POSTGRES_DSN)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self) -> str:
        """Custom function for pretty printing."""
        cols = []
        for ind, col in enumerate(self.__table__.columns.keys()):
            if ind < self.repr_cols_num or col in self.repr_cols:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
