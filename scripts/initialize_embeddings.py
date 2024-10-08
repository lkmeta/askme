import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import FAQ
from app.services.config import settings
from app.services.embeddings import embedding_service  # Import your embedding service

# Set up database URL
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

print("EMBEDDINGS:DATABASE_URL:", DATABASE_URL)

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async session
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def compute_and_store_embeddings():
    print("Computing and storing embeddings...")
    async with SessionLocal() as db:
        try:
            # Compute embeddings using the EmbeddingService and store them directly in the database
            await embedding_service.compute_embeddings(db)
            print("Embeddings computed and stored successfully.")
        except Exception as e:
            print(f"Error computing embeddings: {e}")
            await db.rollback()  # Rollback in case of error


if __name__ == "__main__":
    # Use asyncio to run the compute_and_store_embeddings function
    asyncio.run(compute_and_store_embeddings())
