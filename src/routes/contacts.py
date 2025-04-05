import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.services.contacts import ContactService
from src.schemas.contact import (
    ContactSchema,
    ContactUpdateSchema,
    ContactResponse,
)
from src.services.auth import get_current_user
from src.entity.models import User

router = APIRouter(prefix="/contacts", tags=["contacts"])
logger = logging.getLogger("uvicorn.error")


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    return await service.get_contacts(user_id=user.id, limit=limit, offset=offset)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    contact = await service.get_contact(contact_id, user_id=user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    return await service.create_contact(body, user_id=user.id)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    body: ContactUpdateSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    contact = await service.update_contact(contact_id, body, user_id=user.id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    deleted = await service.remove_contact(contact_id, user_id=user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return None


@router.get("/search/", response_model=list[ContactResponse])
async def search_contacts(
    query: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    return await service.search_contacts(query, user_id=user.id)


@router.get("/birthdays/", response_model=list[ContactResponse])
async def upcoming_birthdays(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    return await service.upcoming_birthdays(user_id=user.id)

