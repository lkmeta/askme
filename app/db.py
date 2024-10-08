from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.services.config import settings

# Set up the database URL from the environment variables
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Set up the async session factory
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Yield the session as an async generator
        finally:
            await session.close()
