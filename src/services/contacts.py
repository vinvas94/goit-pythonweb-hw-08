from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contact import ContactSchema, ContactUpdateSchema


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactSchema):
        return await self.repository.create_contact(body)

    async def get_contacts(self, limit: int, offset: int):
        return await self.repository.get_contacts(limit, offset)

    async def get_contact(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactUpdateSchema):
        return await self.repository.update_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        return await self.repository.remove_contact(contact_id)

    async def search_contacts(self, query: str):
        return await self.repository.search_contacts(query)

    async def upcoming_birthdays(self):
        return await self.repository.upcoming_birthdays()
