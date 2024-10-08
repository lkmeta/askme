from typing import List
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from app.models import FAQ
from app.services.config import settings
from app.utils.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update


class EmbeddingService:
    def __init__(self):
        # Initialize OpenAI embedding model
        self.embeddings_model = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDINGS_MODEL
        )

    async def load_faq_data_from_db(self, db) -> List[FAQ]:
        """
        Load FAQ data asynchronously from the PostgreSQL database using SQLAlchemy.
        """
        try:
            result = await db.execute(select(FAQ))
            faqs = result.scalars().all()  # Get the list of FAQ objects

            logger.info(f"Loaded {len(faqs)} FAQ entries from the database.")
            return faqs
        except Exception as e:

            # Check if the connection is closed
            if db.is_active:
                logger.error(f"The connection is still active: {db.is_active}")

            logger.error(f"Error loading FAQ data: {e}")
            return []

    async def compute_single_embedding(self, question: str):
        """
        Compute the embedding for a single question using the OpenAI embeddings model.
        """
        try:
            embedding = self.embeddings_model.embed_query(question)
            logger.info(f"Computed embedding for the question: {question}")
            return embedding
        except Exception as e:
            logger.error(f"Error computing embedding: {e}")
            return []

    async def compute_embeddings(self, db: AsyncSession):
        """
        Compute embeddings for the FAQ questions and save them directly into the database.
        """

        # Check if the connection is closed
        if not db.is_active:
            logger.error(f"The connection is not active: {db.is_active}")
            return

        try:
            faqs = await self.load_faq_data_from_db(db)
            logger.info(f"Computing embeddings for {len(faqs)} FAQ entries.")
            if not faqs:
                logger.error("No FAQ data found for embedding.")
                return

            documents = []
            for faq in faqs:
                doc = Document(page_content=faq.question, metadata={"faq_entry": faq})
                documents.append(doc)

            # Compute embeddings for all FAQ questions
            embeddings = self.embeddings_model.embed_documents(
                [faq.question for faq in faqs]
            )

            # Update the FAQ entries with the computed embeddings
            for faq, embedding in zip(faqs, embeddings):
                faq.embedding = embedding
                await db.execute(
                    update(FAQ).where(FAQ.id == faq.id).values(embedding=embedding)
                )

            # Commit the updates to the database
            await db.commit()
            logger.info(
                f"Embeddings computed and stored in the database for {len(faqs)} FAQs."
            )
        except Exception as e:
            logger.error(f"Error computing embeddings: {e}")
            await db.rollback()  # Rollback in case of error


embedding_service = EmbeddingService()
