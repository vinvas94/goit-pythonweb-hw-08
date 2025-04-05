from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contact import ContactSchema, ContactUpdateSchema


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactSchema, user_id: int):
        return await self.repository.create_contact(body, user_id)

    async def get_contacts(self, user_id: int, limit: int, offset: int):
        return await self.repository.get_contacts(user_id, limit, offset)

    async def get_contact(self, contact_id: int, user_id: int):
        return await self.repository.get_contact_by_id(contact_id, user_id)

    async def update_contact(self, contact_id: int, body: ContactUpdateSchema, user_id: int):
        return await self.repository.update_contact(contact_id, body, user_id)

    async def remove_contact(self, contact_id: int, user_id: int):
        return await self.repository.remove_contact(contact_id, user_id)

    async def search_contacts(self, query: str, user_id: int):
        return await self.repository.search_contacts(user_id, query)

    async def upcoming_birthdays(self, user_id: int):
        return await self.repository.upcoming_birthdays(user_id)

