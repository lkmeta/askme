import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    EMBEDDINGS_MODEL: str = "text-embedding-3-small"
    SIMILARITY_THRESHOLD: float = 0.7


settings = Settings()
