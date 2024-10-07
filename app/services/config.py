import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()


# Class to store configuration settings for the application
class Settings:
    # OpenAI API key, loaded from environment variables
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    # The model to be used for generating embeddings
    EMBEDDINGS_MODEL: str = "text-embedding-3-small"
    # Threshold for similarity comparison
    SIMILARITY_THRESHOLD: float = 0.7


# Initialize a settings instance to be used across the application
settings = Settings()
