from app.services.embeddings import embedding_service
from app.services.config import settings
from app.utils.logger import logger
from app.models.faq_entry import FAQEntry


class SimilarityService:
    def __init__(self):
        pass  # Remove self.vector_store initialization

    def find_most_similar(self, user_question: str):
        logger.info(f"Finding most similar question for: {user_question}")

        vector_store = embedding_service.vector_store
        if vector_store is None:
            logger.error("Vector store is not loaded.")
            raise ValueError("Vector store is not loaded.")

        # Perform similarity search
        results = vector_store.similarity_search_with_score(user_question, k=1)

        if not results:
            logger.error("No similar questions found.")
            return None, 0.0

        # Get the most similar document and its score
        similar_doc, similarity_score = results[0]

        # Since we're using cosine similarity with normalized embeddings, the score is similarity
        similarity = (
            1 - similarity_score
        )  # For FAISS, similarity_score is distance (1 - cosine_similarity)

        logger.info(f"Similarity score: {similarity}")

        # Reconstruct the FAQEntry object from the metadata
        faq_entry_data = similar_doc.metadata["faq_entry"]
        faq_entry = FAQEntry(**faq_entry_data)

        return faq_entry, similarity

    def is_similar(self, similarity_score: float) -> bool:
        return similarity_score >= settings.SIMILARITY_THRESHOLD


similarity_service = SimilarityService()
