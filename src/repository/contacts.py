import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta

from src.entity.models import Contact
from src.schemas.contact import ContactSchema, ContactUpdateSchema

logger = logging.getLogger("uvicorn.error")


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, user_id: int, limit: int, offset: int) -> Sequence[Contact]:
        stmt = select(Contact).where(Contact.user_id == user_id).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user_id: int) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id, Contact.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_contact(self, body: ContactSchema, user_id: int) -> Contact:
        contact = Contact(**body.model_dump(), user_id=user_id)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int, user_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id, user_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdateSchema, user_id: int
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id, user_id)
        if contact:
            update_data = body.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def search_contacts(self, user_id: int, query: str) -> Sequence[Contact]:
        stmt = select(Contact).where(
            Contact.user_id == user_id,
            (
                Contact.first_name.ilike(f"%{query}%") |
                Contact.last_name.ilike(f"%{query}%") |
                Contact.email.ilike(f"%{query}%")
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def upcoming_birthdays(self, user_id: int) -> Sequence[Contact]:
        today = date.today()
        next_week = today + timedelta(days=7)
        stmt = select(Contact).where(
            Contact.user_id == user_id,
            Contact.birthday.between(today, next_week)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
