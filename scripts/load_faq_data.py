import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models import FAQ
from app.services.config import settings


# Set up database URL
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async session
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def load_faq_data():
    print("Loading FAQ data...")
    async with SessionLocal() as db:
        try:
            # Load the JSON data
            with open("data/faq_data.json", "r", encoding="utf-8") as f:
                faq_data = json.load(f)
                print(f"Loaded {len(faq_data)} FAQ entries.")

            for faq in faq_data:
                # Check if the FAQ entry already exists based on the question
                result = await db.execute(
                    select(FAQ).filter_by(question=faq["question"])
                )
                existing_faq = result.scalars().first()

                if existing_faq:
                    print(f"Skipping duplicate entry: {faq['question']}")
                else:
                    # Insert the new FAQ if not already present
                    new_faq = FAQ(question=faq["question"], answer=faq["answer"])
                    db.add(new_faq)

            await db.commit()
            print("FAQ data loaded successfully.")
        except Exception as e:
            print(f"Error loading FAQ data: {e}")
            await db.rollback()


if __name__ == "__main__":
    asyncio.run(load_faq_data())
