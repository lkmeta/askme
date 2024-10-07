from app.services.embeddings import embedding_service
from app.utils.logger import logger  # Ensure logger is imported

if __name__ == "__main__":
    try:
        embedding_service.compute_embeddings()
        print("Embeddings computed and vector store saved.")
    except Exception as e:
        logger.error(f"Error during embeddings initialization: {e}")
