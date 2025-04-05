import asyncio
import contextlib
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from src.conf.config import settings
from src.entity.models import Base  # Asegúrate de importar Base correctamente

logger = logging.getLogger("uvicorn.error")

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine = create_async_engine(
            url, echo=True, future=True  # Echo a True para ver las consultas SQL
        )
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @contextlib.asynccontextmanager
    async def session(self):
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            await session.rollback()
            raise
        finally:
            await session.close()

    @property
    def engine(self):
        return self._engine


sessionmanager = DatabaseSessionManager(settings.DB_URL)


async def get_db() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session


async def init_db():
    async with sessionmanager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created")

if __name__ == "__main__":
    asyncio.run(init_db())
