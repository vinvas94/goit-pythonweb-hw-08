from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import contacts, auth, users
from src.services.rate_limiter import init_rate_limiter

app = FastAPI(
    title="Contact Manager API",
    version="1.0",
    description="A FastAPI project to manage contacts"
)

# Підключення роутів
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter init
@app.on_event("startup")
async def startup():
    await init_rate_limiter(app)


# Привітальний маршрут
@app.get("/")
def read_root():
    return {"message": "Contact Manager Application v1.0"}


# Перевірка з'єднання з БД
@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result.fetchone() is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Database connected successfully!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error connecting to the database: {str(e)}",
        )
