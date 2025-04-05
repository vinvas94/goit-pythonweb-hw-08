from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.entity.models import User
from src.services.auth import get_current_user
from src.repository.users import UserRepository
from src.services.cloudinary_service import upload_avatar
from src.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    avatar_url = await upload_avatar(file, current_user)
    repo = UserRepository(db)
    updated_user = await repo.update_avatar(current_user, avatar_url)
    return updated_user


@router.get("/confirm-email/{token}")
async def confirm_email(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    from src.services.auth import decode_email_token

    try:
        email = decode_email_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    repo = UserRepository(db)
    await repo.confirm_email(email)
    return {"message": "Email confirmed successfully"}
