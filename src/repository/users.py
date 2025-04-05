from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.schemas.user import UserCreate, UserUpdate
from src.services.auth import get_password_hash


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, body: UserCreate) -> User:
        hashed_password = get_password_hash(body.password)
        user = User(
            username=body.username,
            email=body.email,
            password=hashed_password
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_avatar(self, user: User, avatar_url: str) -> User:
        user.avatar = avatar_url
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def confirm_email(self, email: str) -> None:
        stmt = (
            update(User)
            .where(User.email == email)
            .values(is_verified=True)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def update_user(self, user: User, data: UserUpdate) -> User:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
