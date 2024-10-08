from app.utils.logger import logger
from app.services.config import settings
from app.models import FAQ
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.services.embeddings import embedding_service


class SimilarityService:
    def __init__(self):
        pass

    async def find_most_similar(self, user_question: str, db: AsyncSession):
        """
        Find the most similar question from the FAQ database using pgVector.
        """
        logger.info(f"Finding most similar question for: {user_question}")

        # Generate the embedding for the user question using OpenAI
        embedding = await embedding_service.compute_single_embedding(user_question)

        # SQL query to find the most similar FAQ based on embeddings
        # (using the <=> operator for cosine similarity)
        query = text(
            """
            SELECT id, question, answer, embedding <=> :embedding AS similarity_score
            FROM faqs
            ORDER BY similarity_score
            LIMIT 1;
        """
        )

        try:
            logger.info("Executing similarity search query...")
            result = await db.execute(query, {"embedding": str(embedding)})
            logger.info("Query executed successfully.")
            row = result.fetchone()
            logger.info(f"Row: {row}")

            if row is None:
                return None, 0.0

            id, question, answer, similarity_score = row

            logger.info(f"Found similar question: {question}")

            faq_entry = {"question": question, "answer": answer}

            # Calculate the cosine similarity score from the distance (1 - distance)
            similarity_score = 1 - similarity_score

            return faq_entry, similarity_score
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            raise


# Instantiate the similarity service
similarity_service = SimilarityService()
