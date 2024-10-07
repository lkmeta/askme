import os
import json
from typing import List

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from app.models.faq_entry import FAQEntry
from app.services.config import settings
from app.utils.logger import logger


class EmbeddingService:
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDINGS_MODEL
        )
        self.vector_store_dir = os.path.join("data", "vector_store")
        self.faq_data_path = os.path.join("data", "faq_data.json")
        self.vector_store = None

    def load_faq_data(self) -> List[FAQEntry]:
        with open(self.faq_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        faqs = [FAQEntry(**item) for item in data]
        logger.info(f"Loaded {len(faqs)} FAQ entries.")
        return faqs

    def compute_embeddings(self):
        try:
            faqs = self.load_faq_data()
            documents = []
            for faq in faqs:
                faq_entry_dict = faq.dict()
                doc = Document(
                    page_content=faq.question, metadata={"faq_entry": faq_entry_dict}
                )
                documents.append(doc)

            logger.info("Computing embeddings for questions.")
            self.vector_store = FAISS.from_documents(
                documents=documents, embedding=self.embeddings_model
            )
            self.save_vector_store()
            logger.info("Vector store saved.")
        except Exception as e:
            logger.error(f"Error computing embeddings: {e}")

    def save_vector_store(self):
        os.makedirs(self.vector_store_dir, exist_ok=True)
        self.vector_store.save_local(self.vector_store_dir)
        logger.info("Vector store saved locally.")

    def load_vector_store(self):
        try:
            if os.path.exists(self.vector_store_dir):
                logger.info(f"Loading vector store from {self.vector_store_dir}...")
                self.vector_store = FAISS.load_local(
                    self.vector_store_dir,
                    self.embeddings_model,
                    allow_dangerous_deserialization=True,
                )
                logger.info("Vector store loaded from local.")
            else:
                logger.info("Vector store not found locally. Computing embeddings.")
                self.compute_embeddings()
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise  # Re-raise to see the full traceback


embedding_service = EmbeddingService()
