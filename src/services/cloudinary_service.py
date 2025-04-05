import cloudinary
import cloudinary.uploader
import os
from fastapi import UploadFile

from src.entity.models import User
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


async def upload_avatar(file: UploadFile, user: User) -> str:
    public_id = f"avatars/{user.username}"

    contents = await file.read()

    result = cloudinary.uploader.upload(
        contents,
        public_id=public_id,
        overwrite=True,
        folder="avatars",
        resource_type="image",
    )

    return result.get("secure_url")
