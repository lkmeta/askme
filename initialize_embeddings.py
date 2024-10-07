from app.services.embeddings import embedding_service
from app.utils.logger import logger

# Entry point of the script
if __name__ == "__main__":
    try:
        # Compute embeddings for the FAQ data and save to vector store
        embedding_service.compute_embeddings()
        print("Embeddings computed and vector store saved.")
    except Exception as e:
        # Log any errors that occur during embeddings initialization
        logger.error(f"Error during embeddings initialization: {e}")
