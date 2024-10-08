import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()


# Class to store configuration settings for the application
class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)

    # OpenAI API key, loaded from environment variables
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    # The model to be used for generating embeddings
    EMBEDDINGS_MODEL: str = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")
    # Threshold for similarity comparison
    SIMILARITY_THRESHOLD: float = os.getenv("SIMILARITY_THRESHOLD", 0.7)


# Initialize a settings instance to be used across the application
settings = Settings()
