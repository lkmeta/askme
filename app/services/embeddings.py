import os
import json
from typing import List

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from app.models.faq_entry import FAQEntry
from app.services.config import settings
from app.utils.logger import logger


# Service class for handling embeddings and vector store operations
class EmbeddingService:
    def __init__(self):
        # Initialize the OpenAI embeddings model with API key and model name
        self.embeddings_model = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDINGS_MODEL
        )
        # Set directories for storing vector store and FAQ data
        self.vector_store_dir = os.path.join("data", "vector_store")
        self.faq_data_path = os.path.join("data", "faq_data.json")
        # Placeholder for the vector store
        self.vector_store = None

    def load_faq_data(self) -> List[FAQEntry]:
        """
        Load FAQ data from a JSON file and return as a list of FAQEntry objects.
        """
        with open(self.faq_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        faqs = [FAQEntry(**item) for item in data]
        logger.info(f"Loaded {len(faqs)} FAQ entries.")
        return faqs

    def compute_embeddings(self):
        """
        Compute embeddings for the FAQ questions and save them to a vector store.
        """
        try:
            faqs = self.load_faq_data()
            documents = []
            # Convert each FAQ entry to a Document for embeddings
            for faq in faqs:
                faq_entry_dict = faq.dict()
                doc = Document(
                    page_content=faq.question, metadata={"faq_entry": faq_entry_dict}
                )
                documents.append(doc)

            logger.info("Computing embeddings for questions.")
            # Create a vector store from documents using the embeddings model
            self.vector_store = FAISS.from_documents(
                documents=documents, embedding=self.embeddings_model
            )
            self.save_vector_store()
            logger.info("Vector store saved.")
        except Exception as e:
            logger.error(f"Error computing embeddings: {e}")

    def save_vector_store(self):
        """
        Save the vector store to a local directory for later use.
        """
        os.makedirs(self.vector_store_dir, exist_ok=True)
        self.vector_store.save_local(self.vector_store_dir)
        logger.info("Vector store saved locally.")

    def load_vector_store(self):
        """
        Load the vector store from a local directory. If not found, compute and save embeddings.
        """
        try:
            if os.path.exists(self.vector_store_dir):
                logger.info(f"Loading vector store from {self.vector_store_dir}...")
                self.vector_store = FAISS.load_local(
                    self.vector_store_dir,
                    self.embeddings_model,
                    allow_dangerous_deserialization=True,  # Allow deserialization
                )
                logger.info("Vector store loaded from local.")
            else:
                logger.info("Vector store not found locally. Computing embeddings.")
                self.compute_embeddings()
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise  # Re-raise to see the full traceback


# Instantiate the embedding service for use throughout the application
embedding_service = EmbeddingService()
