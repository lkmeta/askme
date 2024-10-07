from app.services.embeddings import embedding_service
from app.services.config import settings
from app.utils.logger import logger
from app.models.faq_entry import FAQEntry


# A service for finding the most similar question in the FAQ database
class SimilarityService:
    def __init__(self):
        # Initialization (no vector store set here; it's handled in embedding_service)
        pass

    def find_most_similar(self, user_question: str):
        """
        Find the FAQ question that is most similar to the user's question.
        """
        logger.info(f"Finding most similar question for: {user_question}")

        vector_store = embedding_service.vector_store
        if vector_store is None:
            # If the vector store is not loaded, raise an error
            logger.error("Vector store is not loaded.")
            raise ValueError("Vector store is not loaded.")

        # Perform a similarity search in the vector store for the user's question
        results = vector_store.similarity_search_with_score(user_question, k=1)

        # Check if results were found
        if not results:
            logger.error("No similar questions found.")
            return None, 0.0

        # Get the most similar document and its similarity score
        similar_doc, similarity_score = results[0]

        # Convert distance to similarity score (cosine similarity is 1 - distance)
        similarity = 1 - similarity_score

        logger.info(f"Similarity score: {similarity}")

        # Reconstruct the FAQEntry object from the metadata
        faq_entry_data = similar_doc.metadata["faq_entry"]
        faq_entry = FAQEntry(**faq_entry_data)

        return faq_entry, similarity

    def is_similar(self, similarity_score: float) -> bool:
        """
        Check if the similarity score meets or exceeds the defined threshold.
        """
        return similarity_score >= settings.SIMILARITY_THRESHOLD


# Instantiate the similarity service for use in other modules
similarity_service = SimilarityService()
